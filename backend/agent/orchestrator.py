"""
EONIX Agent Orchestrator — The heart of EONIX.
Processes every user command through the full AI pipeline.
"""
import re
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncGenerator, List, Dict, Any, Optional
from dataclasses import dataclass, field

# Thread pool for running blocking (synchronous) tools like Playwright
_tool_executor = ThreadPoolExecutor(max_workers=4)

from brains.ollama_brain import OllamaBrain
from brains.gemini_brain import GeminiBrain
from tools import ToolRegistry
from agent.router import route, parse_brain_prefix
from memory.db import get_db, init_db
from memory.task_store import create_task, update_task, get_recent_tasks
from memory.preference_store import get_preference, set_preference
from memory.semantic import SemanticMemory
from agent.personality import PersonalityEngine
from ai.chatbot import chatbot as chatbot_engine


@dataclass
class AgentResponse:
    reply: str
    brain: str
    actions: List[Dict[str, Any]] = field(default_factory=list)
    duration_ms: int = 0
    task_id: Optional[int] = None
    success: bool = True


class AgentOrchestrator:
    """Main orchestrator — the brain of EONIX."""

    def __init__(self):
        self.ollama = OllamaBrain()
        self.gemini = GeminiBrain()
        self.tools = ToolRegistry()
        self.memory = SemanticMemory()
        self.personality = PersonalityEngine()
        self._default_brain = "auto"

    def _intercept_known_commands(self, text: str) -> Optional[dict]:
        """
        Pattern-match well-known commands and return a hardcoded plan.
        This bypasses the AI for commands where the AI consistently fails.
        Returns a plan dict or None if no match.
        """
        t = text.lower().strip()
        # Keep original case for message extraction
        t_orig = text.strip()

        # ── WhatsApp detection ─────────────────────────────────────
        if "whatsapp" in t:
            # Words that are NOT contact names
            STOPWORDS = {
                "whatsapp", "web", "chrome", "browser", "my", "in", "the", "a",
                "and", "or", "to", "go", "open", "send", "type", "message",
                "contact", "search", "find", "him", "her", "them", "it",
                "please", "now", "then", "after", "new", "start", "chat",
                "write", "say", "with", "via", "on"
            }

            contact = None
            msg = None

            # Pattern 1: "send [msg words] message to [contact]"
            # e.g. "send poda baadey message to muruga"
            m = re.search(r"send\s+([\w][\w\s]{0,50}?)\s+message\s+to\s+([\w]+)", t)
            if m:
                candidate_msg = m.group(1).strip()
                candidate_contact = m.group(2).strip()
                if candidate_contact not in STOPWORDS:
                    msg = candidate_msg
                    contact = candidate_contact

            # Pattern 1b: "send [single word] to [contact]" (short message, no 'message' keyword)
            if not contact:
                m = re.search(r"send\s+([\w]+)\s+to\s+([\w]+)\s+(?:on|via|in|through)\s+whatsapp", t)
                if m:
                    candidate_msg = m.group(1).strip()
                    candidate_contact = m.group(2).strip()
                    if candidate_contact not in STOPWORDS and candidate_msg not in STOPWORDS:
                        msg = candidate_msg
                        contact = candidate_contact

            # Pattern 2: "search [contact]" or "find [contact]"
            if not contact:
                m = re.search(r"(?:search|find)\s+([\w]+)(?:\s+in|\s+on|\s+from)?", t)
                if m and m.group(1).strip() not in STOPWORDS:
                    contact = m.group(1).strip()

            # Pattern 3: "to [contact]" — find last non-stopword after 'to'
            if not contact:
                for m in re.finditer(r"\bto\s+([\w]+)", t):
                    candidate = m.group(1).strip()
                    if candidate not in STOPWORDS:
                        contact = candidate
                        break

            # Pattern 4: "[contact] in my contact"
            if not contact:
                m = re.search(r"([\w]+)\s+in\s+(?:my\s+)?contact", t)
                if m and m.group(1).strip() not in STOPWORDS:
                    contact = m.group(1).strip()

            # Extract message from original text (preserve case)
            if not msg and contact:
                # Try: "send [MSG] message to [contact]" in original case
                m = re.search(rf"send\s+([\w][\w\s]{{0,50}}?)\s+message\s+to\s+{re.escape(contact)}",
                              t_orig, re.IGNORECASE)
                if m:
                    msg = m.group(1).strip()

            # Try: "type [MSG]" or "say [MSG]" or "write [MSG]"
            if not msg:
                for kw in ["type", "say", "write"]:
                    m = re.search(rf"{kw}\s+['\"]?([\w][\w\s]{{0,50}}?)['\"]?\s*(?:message|to|in|$)",
                                  t_orig, re.IGNORECASE)
                    if m:
                        candidate = m.group(1).strip()
                        if candidate.lower() not in STOPWORDS and candidate.lower() != contact:
                            msg = candidate
                            break

            # Fallback: quoted text
            if not msg:
                quoted = re.findall(r"['\"]([^'\"]+)['\"]", t_orig)
                if quoted:
                    msg = quoted[-1]

            # Last fallback: look for common short messages
            if not msg:
                for word in ["hi", "hello", "hey", "ok", "yes", "no"]:
                    if word in t.split():
                        msg = word
                        break
                if not msg:
                    msg = "hi"

            if contact:
                return {
                    "intent": f"Send WhatsApp message to {contact}",
                    "complexity": 0.6,
                    "steps": [{"tool": "send_whatsapp_message",
                               "args": {"contact": contact, "message": msg},
                               "description": f"Open WhatsApp Web, find {contact}, send '{msg}'"}],
                    "response": f"Sending '{msg}' to {contact} on WhatsApp Web..."
                }

        # ── Gmail send ──────────────────────────────────────────────
        # "send email to x@gmail.com saying hello"
        # "email harish@gmail.com subject Test body Hello there"
        if any(w in t for w in ["gmail", "email", "send mail", "send email"]):
            to_m = re.search(r"to\s+([\w._%+\-]+@[\w.\-]+\.\w+)", t)
            subj_m = re.search(r"subject\s+['\"]?(.+?)['\"]?\s*(?:body|saying|message|$)", t)
            body_m = re.search(r"(?:body|saying|message)\s+['\"]?(.+?)['\"]?$", t)
            if to_m:
                to_addr = to_m.group(1)
                subject = subj_m.group(1).strip() if subj_m else "No Subject"
                body = body_m.group(1).strip() if body_m else ""
                return {
                    "intent": f"Send email to {to_addr}",
                    "complexity": 0.5,
                    "steps": [{"tool": "gmail_send",
                               "args": {"to": to_addr, "subject": subject, "body": body},
                               "description": f"Send email to {to_addr}"}],
                    "response": f"Sending email to {to_addr}..."
                }

        # ── Google search ───────────────────────────────────────────
        # "search weather on google" / "google search lofi music"
        google_m = re.search(r"(?:search|google)\s+(.+?)(?:\s+on\s+google|$)", t)
        if google_m and "google" in t and "youtube" not in t:
            query = google_m.group(1).strip()
            return {
                "intent": f"Search Google for: {query}",
                "complexity": 0.2,
                "steps": [{"tool": "google_search",
                           "args": {"query": query},
                           "description": f"Search Google for '{query}'"}],
                "response": f"Searching Google for '{query}'..."
            }

        # ── YouTube search ──────────────────────────────────────────
        # "search lofi music on youtube" / "youtube search coding"
        yt_m = re.search(r"(?:search|youtube)\s+(.+?)(?:\s+on\s+youtube|$)", t)
        if yt_m and "youtube" in t:
            query = yt_m.group(1).strip()
            return {
                "intent": f"Search YouTube for: {query}",
                "complexity": 0.2,
                "steps": [{"tool": "youtube_search",
                           "args": {"query": query},
                           "description": f"Search YouTube for '{query}'"}],
                "response": f"Searching YouTube for '{query}'..."
            }

        return None  # No intercept match

    def _get_memory_context(self, text: str) -> str:
        """Retrieve relevant memories and format them for the AI."""
        try:
            memories = self.memory.retrieve_relevant(text, n_results=3)
            if not memories:
                return ""
            
            context = "\nRelevant Memories:\n"
            for m in memories:
                context += f"- {m['text']}\n"
            return context + "\n"
        except Exception as e:
            print(f"Memory Error: {e}")
            return ""

    async def process(self, user_input: str, conversation_history: List[Dict] = None) -> AgentResponse:
        """Process a user command through the full pipeline."""
        start_time = time.time()
        conversation_history = conversation_history or []

        # 1. Check for slash commands
        if user_input.strip().startswith("/"):
            return self._handle_slash_command(user_input.strip())

        # 2. Parse brain prefix (@local, @gemini)
        forced_brain, clean_input = parse_brain_prefix(user_input)

        # 3. Get DB session and create task record
        db = get_db()
        task = create_task(db, clean_input, "pending")

        # 4. Route to correct brain
        ollama_ok = self.ollama.is_available()
        gemini_ok = self.gemini.is_available()

        effective_brain = forced_brain or self._default_brain
        if effective_brain == "auto" or not effective_brain:
            brain = route(clean_input, forced=None,
                         ollama_available=ollama_ok,
                         gemini_available=gemini_ok)
        else:
            brain = effective_brain

        # Fallback
        if brain == "local" and not ollama_ok:
            brain = "gemini" if gemini_ok else "local"
        if brain == "gemini" and not gemini_ok:
            brain = "local"

        # 5. Execute with chosen brain
        actions = []
        reply = ""

        try:
            # ── Keyword interceptor (bypasses AI for known command patterns) ──
            plan = self._intercept_known_commands(clean_input)
            
            if plan is None:
                # ── MEMORY INJECTION ──
                memory_context = self._get_memory_context(clean_input)
                augmented_input = memory_context + clean_input
                
                if brain == "gemini" and gemini_ok:
                    plan = self.gemini.plan(augmented_input)
                else:
                    plan = self.ollama.plan(augmented_input)
                    brain = "local"

            reply = plan.get("response", "Done!")
            steps = plan.get("steps", [])

            # ── CHATBOT ROUTING ──
            # If no tool steps → it's a general question → route to chatbot
            if not steps and plan is not None:
                try:
                    chat_result = await chatbot_engine.chat(
                        clean_input, conversation_history
                    )
                    reply = chat_result["reply"]
                    brain = chat_result.get("brain", brain)
                except Exception as chat_err:
                    print(f"Chatbot fallback error: {chat_err}")
                    # Keep the original plan response as fallback

            # Execute each step
            loop = asyncio.get_event_loop()
            for step in steps:
                tool_name = step.get("tool", "")
                tool_args = step.get("args", {})
                description = step.get("description", tool_name)

                if not tool_name:
                    continue

                # ── SAFETY CHECK ──
                # Block destructive actions if confirmation is required
                DESTRUCTIVE_TOOLS = ["delete_file", "remove_file", "shutdown", "reboot"]
                is_destructive = any(dt in tool_name for dt in DESTRUCTIVE_TOOLS) or \
                                ("delete" in description.lower()) or \
                                ("shutdown" in description.lower())
                
                # Check config.REQUIRE_CONFIRMATION (default false for now)
                from config import REQUIRE_CONFIRMATION
                if is_destructive and REQUIRE_CONFIRMATION:
                    # In a real app, we'd emit a confirmation request event
                    reply = f"⚠️ Safety Stop: I need your confirmation to execute '{tool_name}' ({description}). Action blocked."
                    actions.append({
                        "tool": tool_name,
                        "success": False, 
                        "result": "Blocked by safety setting"
                    })
                    continue

                # Run blocking tool in thread pool so we don't block the event loop
                result = await loop.run_in_executor(
                    _tool_executor,
                    lambda tn=tool_name, ta=tool_args: self.tools.execute(tn, ta)
                )
                action_record = {
                    "tool": tool_name,
                    "args": tool_args,
                    "description": description,
                    "result": str(result),
                    "success": result.success
                }
                actions.append(action_record)

                # If a critical step fails, note it
                if not result.success:
                    reply = f"I encountered an issue: {result.message}. " + reply

        except Exception as e:
            reply = f"I ran into an error processing your request: {str(e)}"
            brain = brain

        # 6. Calculate duration and update task record
        duration_ms = int((time.time() - start_time) * 1000)
        success = all(a.get("success", True) for a in actions) if actions else True

        update_task(db, task.id,
                   brain_used=brain,
                   intent=plan.get("intent", "") if 'plan' in dir() else "",
                   plan=plan.get("steps", []) if 'plan' in dir() else [],
                   actions=actions,
                   result=reply,
                   success=success,
                   duration_ms=duration_ms)
        db.close()

        return AgentResponse(
            reply=reply,
            brain=brain,
            actions=actions,
            duration_ms=duration_ms,
            task_id=task.id,
            success=success
        )

    async def stream_process(self, user_input: str, conversation_history: List[Dict] = None) -> AsyncGenerator[Dict, None]:
        """Stream the processing with real-time updates."""
        start_time = time.time()

        # Check slash commands
        if user_input.strip().startswith("/"):
            result = self._handle_slash_command(user_input.strip())
            yield {"type": "complete", "reply": result.reply, "brain": result.brain,
                   "actions": [], "duration_ms": 0}
            return

        forced_brain, clean_input = parse_brain_prefix(user_input)
        ollama_ok = self.ollama.is_available()
        gemini_ok = self.gemini.is_available()

        effective_brain = forced_brain or self._default_brain
        if effective_brain == "auto" or not effective_brain:
            brain = route(clean_input, forced=None, ollama_available=ollama_ok, gemini_available=gemini_ok)
        else:
            brain = effective_brain

        if brain == "local" and not ollama_ok:
            brain = "gemini" if gemini_ok else "local"
        if brain == "gemini" and not gemini_ok:
            brain = "local"

        yield {"type": "thinking", "brain": brain, "message": f"Thinking with {brain.upper()} brain..."}

        # Get plan — try keyword interceptor first
        try:
            plan = self._intercept_known_commands(clean_input)
            
            if plan is None:
                # ── MEMORY + MOOD INJECTION ──
                memory_context = self._get_memory_context(clean_input)
                mood = self.personality.detect_mood(clean_input)
                tone = self.personality.get_tone_instruction(mood)
                time_ctx = self.personality.get_time_context()
                
                mood_context = f"\n[Mood: {mood}. Tone: {tone}. {time_ctx}]\n"
                augmented_input = mood_context + memory_context + clean_input

                if brain == "gemini" and gemini_ok:
                    plan = self.gemini.plan(augmented_input)
                else:
                    plan = self.ollama.plan(augmented_input)
                    brain = "local"
        except Exception as e:
            yield {"type": "complete", "reply": f"Error: {str(e)}", "brain": brain, "actions": [], "duration_ms": 0}
            return

        steps = plan.get("steps", [])
        reply = plan.get("response", "Done!")
        actions = []

        # ── CHATBOT ROUTING ──
        # If no tool steps → it's a general question → route to chatbot
        if not steps:
            try:
                yield {"type": "thinking", "brain": brain, "message": "Crafting a thoughtful response..."}
                chat_result = await chatbot_engine.chat(
                    clean_input, conversation_history
                )
                reply = chat_result["reply"]
                brain = chat_result.get("brain", brain)
            except Exception as chat_err:
                print(f"Chatbot fallback error: {chat_err}")
                # Keep the original plan response as fallback

        # Execute steps and stream updates
        db = get_db()
        task = create_task(db, clean_input, brain)
        loop = asyncio.get_event_loop()

        for i, step in enumerate(steps):
            tool_name = step.get("tool", "")
            tool_args = step.get("args", {})
            description = step.get("description", tool_name)

            if not tool_name:
                continue

            yield {"type": "action_start", "step": i + 1, "total": len(steps),
                   "tool": tool_name, "description": description, "args": tool_args}

            # Run blocking tool in thread pool so we don't block the event loop
            result = await loop.run_in_executor(
                _tool_executor,
                lambda tn=tool_name, ta=tool_args: self.tools.execute(tn, ta)
            )
            action_record = {
                "tool": tool_name,
                "args": tool_args,
                "description": description,
                "result": str(result),
                "success": result.success
            }
            actions.append(action_record)

            yield {"type": "action", "tool": tool_name, "args": tool_args,
                   "result": str(result), "success": result.success,
                   "step": i + 1, "total": len(steps)}

            # Small delay between steps for UI readability
            await asyncio.sleep(0.1)

        duration_ms = int((time.time() - start_time) * 1000)
        success = all(a.get("success", True) for a in actions) if actions else True

        update_task(db, task.id,
                   brain_used=brain,
                   intent=plan.get("intent", ""),
                   plan=steps,
                   actions=actions,
                   result=reply,
                   success=success,
                   duration_ms=duration_ms)
        db.close()

        yield {"type": "complete", "reply": reply, "brain": brain,
               "actions": actions, "duration_ms": duration_ms, "task_id": task.id}

    def _handle_slash_command(self, cmd: str) -> AgentResponse:
        """Handle built-in slash commands."""
        parts = cmd.split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        if command == "/help":
            reply = """**EONIX Slash Commands:**
• `/help` — Show this help
• `/status` — System status (CPU, RAM, battery)
• `/memory` — Show last 10 tasks
• `/brain local` — Use Ollama (fast, offline)
• `/brain gemini` — Use Gemini (powerful, needs internet)
• `/brain auto` — Auto-select brain
• `/briefing` — Get your daily briefing
• `/clear` — Clear chat history
• `/preferences` — Show stored preferences"""

        elif command == "/status":
            from tools.system_info import SystemInfo
            si = SystemInfo()
            data = si.get_all()
            cpu = data['cpu']
            mem = data['memory']
            disk = data['disk']
            battery = data.get('battery')
            ollama_status = "🟢 Online" if self.ollama.is_available() else "🔴 Offline"
            gemini_status = "🟢 Online" if self.gemini.is_available() else "🔴 Offline"
            reply = f"""**System Status:**
• CPU: {cpu['percent']}% ({cpu['cores']} cores)
• RAM: {mem['used_gb']}GB / {mem['total_gb']}GB ({mem['percent']}%)
• Disk: {disk['used_gb']}GB / {disk['total_gb']}GB ({disk['percent']}%)
• Battery: {f"{battery['percent']}% ({'charging' if battery['plugged'] else 'on battery'})" if battery else 'Desktop (no battery)'}

**AI Brains:**
• Ollama (Local): {ollama_status}
• Gemini: {gemini_status}
• Active Brain: {self._default_brain.upper()}"""

        elif command == "/memory":
            db = get_db()
            tasks = get_recent_tasks(db, limit=10)
            db.close()
            if not tasks:
                reply = "No tasks in memory yet."
            else:
                lines = ["**Recent Tasks:**"]
                for t in tasks:
                    status = "✓" if t.success else "✗" if t.success is False else "?"
                    lines.append(f"• [{status}] {t.user_input[:60]}... ({t.brain_used})")
                reply = "\n".join(lines)

        elif command == "/brain":
            if args:
                brain = args[0].lower()
                if brain in ("local", "ollama"):
                    self._default_brain = "local"
                    reply = "🧠 Switched to **LOCAL** brain (Ollama/Mistral)"
                elif brain in ("gemini", "google"):
                    self._default_brain = "gemini"
                    reply = "🧠 Switched to **GEMINI** brain"
                elif brain == "auto":
                    self._default_brain = "auto"
                    reply = "🧠 Switched to **AUTO** brain routing"
                else:
                    reply = f"Unknown brain: {brain}. Use: local, gemini, auto"
            else:
                reply = f"Current brain: **{self._default_brain.upper()}**\nUsage: /brain [local|gemini|auto]"

        elif command == "/clear":
            reply = "__CLEAR_CHAT__"

        elif command == "/preferences":
            db = get_db()
            from memory.preference_store import get_all_preferences
            prefs = get_all_preferences(db)
            db.close()
            if not prefs:
                reply = "No preferences stored yet."
            else:
                lines = ["**Stored Preferences:**"]
                for k, v in prefs.items():
                    lines.append(f"• {k}: {v}")
                reply = "\n".join(lines)

        elif command == "/briefing":
            from agent.briefing import daily_briefing
            import asyncio
            briefing = asyncio.get_event_loop().run_until_complete(daily_briefing.generate())
            reply = daily_briefing.format_text(briefing)

        else:
            reply = f"Unknown command: {cmd}\nType `/help` for available commands."

        return AgentResponse(reply=reply, brain="system", success=True)

    def set_default_brain(self, brain: str):
        self._default_brain = brain


# Singleton instance
orchestrator = AgentOrchestrator()
