"""
EONIX Agent Orchestrator — The heart of EONIX.
Processes every user command through the full AI pipeline.
"""
import re
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncGenerator, List, Dict, Any, Optional, cast
from dataclasses import dataclass, field

# Thread pool for running blocking (synchronous) tools like Playwright
# must be 1 to use persistent sync_playwright session safely
_tool_executor = ThreadPoolExecutor(max_workers=1)

# Initialize placeholders
OllamaBrain = None
GeminiBrain = None
ToolRegistry = None
route = None
parse_brain_prefix = None
get_db = None
init_db = None
create_task = None
update_task = None
get_recent_tasks = None
get_preference = None
set_preference = None
semantic_memory = None
PersonalityEngine = None
chatbot_engine = None

try:
    from brains.ollama_brain import OllamaBrain
    from brains.gemini_brain import GeminiBrain
    from brains.claude_brain import ClaudeBrain
    from tools import ToolRegistry
    from agent.router import route, parse_brain_prefix
    from memory.db import get_db, init_db
    from memory.task_store import create_task, update_task, get_recent_tasks
    from memory.preference_store import get_preference, set_preference
    from memory.preference_store import get_preference, set_preference
    from memory.semantic import semantic_memory
    from memory.episodic import episodic_memory
    from agent.personality import PersonalityEngine
    from ai.chatbot import chatbot as chatbot_engine
except Exception:
    import traceback
    traceback.print_exc()


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
        self.ollama = OllamaBrain() if OllamaBrain else None
        self.gemini = GeminiBrain() if GeminiBrain else None
        self.claude = ClaudeBrain() if ClaudeBrain else None
        self.tools = ToolRegistry() if ToolRegistry else None
        self.memory = semantic_memory
        self.personality = PersonalityEngine() if PersonalityEngine else None
        self._default_brain = "auto"

    def _intercept_known_commands(self, text: str) -> Optional[Dict[str, Any]]:
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

            # ── NEW: YouTube + WhatsApp chaining ──
            # "send recent [QUERY] video to [CONTACT]"
            # "search [QUERY] video and send to [CONTACT]"
            yt_chain_m = re.search(r"(?:search|send)\s+(?:recent\s+)?(.*?)\s+video\s+(?:to|and\s+send\s+to)\s+([\w]+)", t)
            if yt_chain_m:
                yt_query = yt_chain_m.group(1).strip()
                contact = yt_chain_m.group(2).strip()
                if contact not in STOPWORDS:
                    return {
                        "intent": f"Search YouTube for '{yt_query}' and send to {contact}",
                        "complexity": 0.8,
                        "steps": [
                            {"tool": "youtube_search",
                             "args": {"query": yt_query},
                             "description": f"Search YouTube for {yt_query}"},
                            {"tool": "send_whatsapp_message",
                             "args": {"contact": contact, "message": "Here is the video: {{last_result.data.url}}"},
                             "description": f"Send video link to {contact}"}
                        ],
                        "response": f"Sure! Searching for '{yt_query}' video and sending it to {contact}..."
                    }

            # ── Existing WhatsApp extraction logic (Refined) ──
            # Pattern 1: "send [msg words] message to [contact]"
            m = re.search(r"send\s+(.*?)\s+message\s+to\s+([\w]+)", t)
            if m:
                contact = m.group(2).strip()
                if contact not in STOPWORDS:
                    msg = m.group(1).strip()

            # Pattern 1b: "send [msg] to [contact]"
            if not contact:
                m = re.search(r"send\s+(.*?)\s+to\s+([\w]+)\s+(?:on|via|in|through)\s+whatsapp", t)
                if m:
                    msg = m.group(1).strip()
                    contact = m.group(2).strip()

            # Pattern 2: "search [contact]"
            if not contact:
                m = re.search(r"(?:search|find)\s+([\w]+)", t)
                if m and m.group(1).strip() not in STOPWORDS:
                    contact = m.group(1).strip()

            # Extract message from original text (preserve case and flexibility)
            if not msg and contact:
                # Try to find what else the user said besides the contact and the "send to" command
                junk = [contact.lower(), "send", "to", "whatsapp", "in", "on", "via", "message"]
                words = t_orig.split()
                msg_words = [w for w in words if w.lower() not in junk]
                if msg_words:
                    msg = " ".join(msg_words)

            if contact:
                if not msg or msg.lower() in STOPWORDS:
                     msg = "hi" # Ultimate fallback
                
                return {
                    "intent": f"Send WhatsApp message to {contact}",
                    "complexity": 0.6,
                    "steps": [{"tool": "browser_action",
                               "args": {"action": "whatsapp_send", "contact": contact, "message": msg},
                               "description": f"Open WhatsApp Web, find {contact}, send '{msg}'"}],
                    "response": f"Sending '{msg}' to {contact} on WhatsApp Web..."
                }

        # ── Git command interception ─────────────────────────────────
        # "git status", "check git", "pull code", "push changes"
        if "git" in t or "commit" in t or "push" in t or "pull" in t:
            if "status" in t or "check" in t:
                return {
                    "intent": "Check git status",
                    "complexity": 0.2,
                    "steps": [{"tool": "git_action", "args": {"action": "status"}, "description": "Check git status"}],
                    "response": "Checking git status..."
                }
            if "log" in t or "history" in t:
                return {
                    "intent": "Check git history",
                    "complexity": 0.2,
                    "steps": [{"tool": "git_action", "args": {"action": "log", "limit": "10"}, "description": "Show recent git log"}],
                    "response": "Fetching git history..."
                }
            if "pull" in t:
                return {
                    "intent": "Pull latest code",
                    "complexity": 0.3,
                    "steps": [{"tool": "git_action", "args": {"action": "pull"}, "description": "Pull latest changes from remote"}],
                    "response": "Pulling latest changes..."
                }
            if "push" in t:
                return {
                    "intent": "Push code to remote",
                    "complexity": 0.3,
                    "steps": [{"tool": "git_action", "args": {"action": "push"}, "description": "Push local commits to remote"}],
                    "response": "Pushing changes to remote..."
                }
            if "commit" in t:
                # extract message: "commit with message 'fix bug'" or "commit saying 'fix bug'"
                msg_m = re.search(r"['\"](.*?)['\"]", t)
                msg = msg_m.group(1) if msg_m else "Update"
                return {
                    "intent": f"Commit changes with message '{msg}'",
                    "complexity": 0.3,
                    "steps": [
                        {"tool": "git_action", "args": {"action": "add", "files": "."}, "description": "Stage all files"},
                        {"tool": "git_action", "args": {"action": "commit", "message": msg}, "description": f"Commit with message: {msg}"}
                    ],
                    "response": f"Committing changes with message '{msg}'..."
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

        # ── App Control (Open/Close) ───────────────────────────────
        # Intercept ONLY simple commands. Let LLM handle complex ones ("open notepad and type hi")
        # "open notepad", "launch calculator", "start chrome"
        
        # Check for multi-step indicators
        if " and " in t or " then " in t or "," in t:
            return None

        # Open
        open_m = re.search(r"^(?:open|launch|start|run)\s+(.+?)$", t)
        if open_m:
            app = open_m.group(1).strip()
            # Filter out some common non-apps if needed, but usually safe
            if app not in ["it", "that", "the", "a", "an"]:
                return {
                    "intent": f"Open application: {app}",
                    "complexity": 0.1,
                    "steps": [{"tool": "open_application",
                               "args": {"app_name": app},
                               "description": f"Launch {app}"}],
                    "response": f"Opening {app}..."
                }

        # Close
        close_m = re.search(r"^(?:close|quit|exit|terminate|kill)\s+(.+?)$", t)
        if close_m:
            app = close_m.group(1).strip()
            if app not in ["it", "that", "me"]:
                 return {
                    "intent": f"Close application: {app}",
                    "complexity": 0.1,
                    "steps": [{"tool": "close_application",
                               "args": {"app_name": app},
                               "description": f"Close {app}"}],
                    "response": f"Closing {app}..."
                }

        # ── Weather ───────────────────────────────────────────────
        weather_m = re.search(r"(?:weather|temperature|temp)\s*(?:in|at|for|of)?\s*(\w[\w\s]*)?", t)
        if weather_m and ("weather" in t or "temperature" in t):
            city = (weather_m.group(1) or "auto").strip()
            return {
                "intent": f"Check weather in {city}",
                "complexity": 0.1,
                "steps": [{"tool": "check_weather", "args": {"city": city},
                           "description": f"Get weather for {city}"}],
                "response": f"Checking weather for {city}..."
            }

        # ── Spotify / Music ───────────────────────────────────────
        if any(w in t for w in ["play music", "pause music", "next song", "previous song",
                                "play spotify", "pause spotify", "resume music", "skip song",
                                "stop music"]):
            if "next" in t or "skip" in t:
                action = "next"
            elif "prev" in t or "back" in t:
                action = "previous"
            elif "pause" in t or "stop" in t:
                action = "pause"
            else:
                action = "play"
            return {
                "intent": f"Music control: {action}",
                "complexity": 0.1,
                "steps": [{"tool": "spotify_control", "args": {"action": action},
                           "description": f"Media: {action}"}],
                "response": f"⏯ {action.capitalize()}ing music..."
            }
        play_m = re.search(r"play\s+(.+?)(?:\s+on\s+spotify)?$", t)
        if play_m and "spotify" in t:
            query = play_m.group(1).replace("on spotify", "").strip()
            return {
                "intent": f"Search Spotify for {query}",
                "complexity": 0.2,
                "steps": [{"tool": "spotify_control", "args": {"action": "search", "query": query},
                           "description": f"Search Spotify for {query}"}],
                "response": f"🎵 Searching Spotify for '{query}'..."
            }

        # ── Reminders & Alarms ────────────────────────────────────
        remind_m = re.search(r"(?:remind me|set (?:a )?reminder|alarm)\s*(?:to|for|about)?\s*(.+)", t)
        if remind_m:
            from tools.reminder import ReminderTool
            parsed = ReminderTool.parse_time_from_text(remind_m.group(1).strip())
            return {
                "intent": f"Set reminder: {parsed['text']}",
                "complexity": 0.1,
                "steps": [{"tool": "set_reminder",
                           "args": {"text": parsed["text"], "minutes": parsed["minutes"], "time_str": parsed["time_str"]},
                           "description": f"Remind: {parsed['text']}"}],
                "response": f"⏰ Setting reminder: {parsed['text']}..."
            }
        if "my reminders" in t or "list reminders" in t or "show reminders" in t:
            return {
                "intent": "List reminders",
                "complexity": 0.1,
                "steps": [{"tool": "list_reminders", "args": {}, "description": "List active reminders"}],
                "response": "Checking your reminders..."
            }

        # ── Lock / Shutdown / Restart ─────────────────────────────
        if re.search(r"\b(lock|shutdown|shut down|restart|reboot|sleep)\b.*\b(pc|computer|laptop|system|machine)?\b", t):
            if "lock" in t:
                action = "lock"
            elif "restart" in t or "reboot" in t:
                action = "restart"
            elif "sleep" in t:
                action = "sleep"
            elif "shut" in t:
                action = "shutdown"
            else:
                action = "lock"
            return {
                "intent": f"Power: {action}",
                "complexity": 0.1,
                "steps": [{"tool": "power_action", "args": {"action": action},
                           "description": f"{action.capitalize()} the PC"}],
                "response": f"{'🔒' if action == 'lock' else '⏻'} {action.capitalize()}ing your PC..."
            }

        # ── Screenshot & Describe ─────────────────────────────────
        if re.search(r"(screenshot|screen.?shot|what.?s on (?:my )?screen|describe.* screen|capture.* screen)", t):
            if "describe" in t or "what" in t or "read" in t:
                return {
                    "intent": "Describe screen",
                    "complexity": 0.3,
                    "steps": [{"tool": "describe_screen", "args": {"question": "Describe what is on my screen"},
                               "description": "Describe screen contents"}],
                    "response": "📸 Analyzing your screen..."
                }
            return {
                "intent": "Take screenshot",
                "complexity": 0.1,
                "steps": [{"tool": "take_screenshot", "args": {},
                           "description": "Take a screenshot"}],
                "response": "📸 Taking screenshot..."
            }

        # ── Notes ─────────────────────────────────────────────────
        note_m = re.search(r"(?:create|make|write|add)\s+(?:a )?note\s*(?:called|titled|named)?\s*(.+)", t)
        if note_m:
            title = note_m.group(1).strip()
            return {
                "intent": f"Create note: {title}",
                "complexity": 0.1,
                "steps": [{"tool": "create_note", "args": {"title": title, "content": ""},
                           "description": f"Create note '{title}'"}],
                "response": f"📝 Creating note '{title}'..."
            }
        if re.search(r"(read|show|list|view)\s*(my )?(notes|note)", t):
            return {
                "intent": "List notes",
                "complexity": 0.1,
                "steps": [{"tool": "read_notes", "args": {}, "description": "List all notes"}],
                "response": "📋 Reading your notes..."
            }

        # ── Gmail Send ────────────────────────────────────────────
        email_m = re.search(r"(?:send|compose|write)\s+(?:an? )?email\s+to\s+(\S+)\s*(?:saying|with|about|subject)?\s*(.*)", t)
        if email_m:
            to_email = email_m.group(1).strip()
            body = email_m.group(2).strip() or "Hello"
            return {
                "intent": f"Send email to {to_email}",
                "complexity": 0.5,
                "steps": [{"tool": "gmail_send", "args": {"to": to_email, "subject": "Message from EONIX", "body": body},
                           "description": f"Send email to {to_email}"}],
                "response": f"📧 Sending email to {to_email}..."
            }

        # ── Webpage Read/Summarize ────────────────────────────────
        url_m = re.search(r"(?:read|summarize|summarise|fetch)\s+(?:this )?(?:page|url|website|article|webpage)?\s*(https?://\S+)", t)
        if url_m:
            url = url_m.group(1).strip()
            return {
                "intent": f"Read webpage: {url}",
                "complexity": 0.4,
                "steps": [{"tool": "read_webpage", "args": {"url": url},
                           "description": f"Fetch and read {url}"}],
                "response": f"📄 Reading {url}..."
            }

        return None  # No intercept match


    def _get_memory_context(self, text: str) -> str:
        """Retrieve relevant memories and format them for the AI."""
        context = ""
        try:
            # 1. Episodic (Recent Context)
            recents = episodic_memory.get_recent(limit=5)
            if recents:
                context += "\n[Recent Conversation]:\n"
                for r in recents:
                    context += f"User: {r['user']}\nEonix: {r['agent']}\n"
            
            # 2. Semantic (Relevant Facts)
            memories = self.memory.retrieve_relevant(text, n_results=3)
            if memories:
                context += "\n[Relevant Notes]:\n"
                for m in memories:
                    context += f"- {m['text']}\n"
            
            return context + "\n" if context else ""
        except Exception as e:
            print(f"Memory Error: {e}")
            return ""

    async def process(self, user_input: str, conversation_history: Optional[List[Dict[str, Any]]] = None, brain_override: Optional[str] = None) -> AgentResponse:
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
        ollama_ok = self.ollama.is_available() if self.ollama else False
        gemini_ok = self.gemini.is_available() if self.gemini else False
        claude_ok = self.claude.is_available() if self.claude else False

        effective_brain = forced_brain or brain_override or self._default_brain
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
        actions: List[Dict[str, Any]] = []
        reply = ""

        plan_raw: Dict[str, Any] = {}
        try:
            # ── Keyword interceptor (bypasses AI for known command patterns) ──
            intercepted = self._intercept_known_commands(clean_input)
            
            if intercepted is not None:
                plan_raw = intercepted
            else:
                # ── MEMORY INJECTION ──
                memory_context = self._get_memory_context(clean_input)
                augmented_input = memory_context + clean_input
                
                if brain == "gemini" and gemini_ok and self.gemini:
                    plan_raw = await self.gemini.plan(augmented_input)
                elif brain == "claude" and claude_ok and self.claude:
                    plan_raw = await self.claude.plan(augmented_input)
                elif self.ollama:
                    plan_raw = await self.ollama.plan(augmented_input)
                    brain = "local"
                else:
                    plan_raw = {"response": "No AI brain available.", "steps": []}

            plan = cast(Dict[str, Any], plan_raw)
            reply = plan.get("response", "Done!")
            steps = plan.get("steps", [])

            # ── CHATBOT ROUTING ──
            # If no tool steps → it's a general question → route to chatbot
            if not steps:
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
            loop = cast(Any, asyncio.get_event_loop())
            for i, step in enumerate(steps):
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
                try:
                    from config import REQUIRE_CONFIRMATION
                except ImportError:
                    REQUIRE_CONFIRMATION = False

                if is_destructive and REQUIRE_CONFIRMATION:
                    # In a real app, we'd emit a confirmation request event
                    reply = f"⚠️ Safety Stop: I need your confirmation to execute '{tool_name}' ({description}). Action blocked."
                    actions.append({
                        "tool": tool_name,
                        "success": False, 
                        "result": "Blocked by safety setting"
                    })
                    continue

                # ── RESULT INTERPOLATION ──
                # If args contain {{last_result...}}, replace with data from previous step
                if i > 0 and actions:
                    last_action = actions[-1]
                    last_res_obj = last_action.get("result_obj")
                    if last_res_obj:
                        import json
                        # Convert args to string, replace, and back to dict
                        args_str = json.dumps(tool_args)
                        if "{{last_result.data.url}}" in args_str and getattr(last_res_obj, 'data', {}).get('url'):
                            args_str = args_str.replace("{{last_result.data.url}}", last_res_obj.data['url'])
                        if "{{last_result.message}}" in args_str:
                             args_str = args_str.replace("{{last_result.message}}", getattr(last_res_obj, 'message', ''))
                        tool_args = json.loads(args_str)

                # Run blocking tool in thread pool so we don't block the event loop
                if self.tools:
                    result = await loop.run_in_executor(
                        _tool_executor,
                        lambda tn=tool_name, ta=tool_args: self.tools.execute(tn, ta)
                    )
                else:
                    from types import SimpleNamespace
                    result = SimpleNamespace(success=False, message="Tool Registry not available")

                action_record = {
                    "tool": tool_name,
                    "args": tool_args,
                    "description": description,
                    "result": str(result),
                    "result_obj": result, # Store the full object for interpolation
                    "success": getattr(result, 'success', False)
                }
                actions.append(action_record)

                # If a critical step fails, note it
                if not result.success:
                    reply = f"I encountered an issue: {result.message}. " + str(reply)

        except Exception as e:
            reply = f"I ran into an error processing your request: {str(e)}"
            brain = brain

        # 6. Calculate duration and update task record
        duration_ms = int((time.time() - start_time) * 1000)
        success = all(a.get("success", True) for a in actions) if actions else True

        update_task(db, task.id,
                   brain_used=brain,
                   intent=plan.get("intent", ""),
                   plan=plan.get("steps", []),
                   actions=actions,
                   result=reply,
                   success=success,
                   duration_ms=duration_ms)
        db.close()

        # ── AUTO-SAVE EPISODIC MEMORY ──
        if episodic_memory:
            episodic_memory.save_turn(clean_input, reply, tags=[brain])

        return AgentResponse(
            reply=reply,
            brain=brain,
            actions=actions,
            duration_ms=duration_ms,
            task_id=task.id,
            success=success
        )

    async def stream_process(self, user_input: str, conversation_history: Optional[List[Dict[str, Any]]] = None, brain_override: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream the processing with real-time updates."""
        start_time = time.time()

        # Check slash commands
        if user_input.strip().startswith("/"):
            result = self._handle_slash_command(user_input.strip())
            yield {"type": "complete", "reply": result.reply, "brain": result.brain,
                   "actions": [], "duration_ms": 0}
            return

        forced_brain, clean_input = parse_brain_prefix(user_input)
        ollama_ok = self.ollama.is_available() if self.ollama else False
        gemini_ok = self.gemini.is_available() if self.gemini else False

        effective_brain = forced_brain or brain_override or self._default_brain
        if effective_brain == "auto" or not effective_brain:
            brain = route(clean_input, forced=None, ollama_available=ollama_ok, gemini_available=gemini_ok)
        else:
            brain = effective_brain

        if brain == "local" and not ollama_ok:
            brain = "gemini" if gemini_ok else "local"
        if brain == "gemini" and not gemini_ok:
            brain = "local"

        yield {"type": "thinking", "brain": brain, "status": "initializing", "message": f"Contacting {brain.upper()} brain... (This may take a moment)"}

        # Get plan — try keyword interceptor first
        plan: Dict[str, Any] = {}
        try:
            intercepted = self._intercept_known_commands(clean_input)
            
            if intercepted is not None:
                plan = intercepted
            else:
                # ── MEMORY + MOOD INJECTION ──
                memory_context = self._get_memory_context(clean_input)
                mood = self.personality.detect_mood(clean_input)
                tone = self.personality.get_tone_instruction(mood)
                time_ctx = self.personality.get_time_context()
                
                mood_context = f"\n[Mood: {mood}. Tone: {tone}. {time_ctx}]\n"
                augmented_input = mood_context + memory_context + clean_input

                if brain == "gemini" and gemini_ok and self.gemini:
                    plan = await self.gemini.plan(augmented_input)
                elif self.ollama:
                    yield {"type": "thinking", "brain": "local", "status": "planning", "message": "Ollama is planning steps..."}
                    plan = await self.ollama.plan(augmented_input)
                    brain = "local"
                else:
                    plan = {"response": "No AI brain available.", "steps": []}
        except Exception as e:
            yield {"type": "complete", "reply": f"Error: {str(e)}", "brain": brain, "actions": [], "duration_ms": 0}
            return

        steps = plan.get("steps", [])
        reply = plan.get("response", "Done!")
        actions: List[Dict[str, Any]] = []

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
        loop = cast(Any, asyncio.get_event_loop())

        for i, step in enumerate(steps):
            tool_name = step.get("tool", "")
            tool_args = step.get("args", {})
            description = step.get("description", tool_name)

            if not tool_name:
                continue

            # ── RESULT INTERPOLATION ──
            if i > 0 and actions:
                last_action = actions[-1]
                last_res_obj = last_action.get("result_obj")
                if last_res_obj:
                    import json
                    args_str = json.dumps(tool_args)
                    if "{{last_result.data.url}}" in args_str and getattr(last_res_obj, 'data', {}).get('url'):
                        args_str = args_str.replace("{{last_result.data.url}}", last_res_obj.data['url'])
                    if "{{last_result.message}}" in args_str:
                         args_str = args_str.replace("{{last_result.message}}", getattr(last_res_obj, 'message', ''))
                    tool_args = json.loads(args_str)

            yield {"type": "action_start", "step": i + 1, "total": len(steps),
                   "tool": tool_name, "description": description, "args": tool_args}

            # Run blocking tool in thread pool so we don't block the event loop
            if self.tools:
                result = await loop.run_in_executor(
                    _tool_executor,
                    lambda tn=tool_name, ta=tool_args: self.tools.execute(tn, ta)
                )
            else:
                from types import SimpleNamespace
                result = SimpleNamespace(success=False, message="Tool Registry not available")

            action_record = {
                "tool": tool_name,
                "args": tool_args,
                "description": description,
                "result": str(result),
                "result_obj": result,
                "success": getattr(result, 'success', False)
            }
            actions.append(action_record)

            yield {"type": "action", "tool": tool_name, "args": tool_args,
                   "result": str(result), "success": result.success,
                   "step": i + 1, "total": len(steps)}

            # Small delay between steps for UI readability
            await asyncio.sleep(0.1)

        # ── Update reply with actual tool results ──
        if actions:
            successful = [a for a in actions if a.get("success")]
            if successful:
                # Use the last successful tool's result as the reply
                last_result = successful[-1].get("result_obj")
                if last_result and hasattr(last_result, "message") and last_result.message:
                    reply = last_result.message
            elif not all(a.get("success", True) for a in actions):
                # All failed: collect error messages
                errors = [a.get("result", "Unknown error") for a in actions if not a.get("success")]
                reply = "❌ " + "; ".join(errors)

        duration_ms = int((time.time() - start_time) * 1000)
        success = all(a.get("success", True) for a in actions) if actions else True

        # Strip non-serializable objects before DB save and SSE yield
        serializable_actions = [
            {k: v for k, v in a.items() if k != "result_obj"} for a in actions
        ]

        try:
            update_task(db, task.id,
                       brain_used=brain,
                       intent=plan.get("intent", ""),
                       plan=steps,
                       actions=serializable_actions,
                       result=reply,
                       success=success,
                       duration_ms=duration_ms)
            db.close()
        except Exception as db_err:
            print(f"[WARN] update_task error: {db_err}")

        # ── AUTO-SAVE EPISODIC MEMORY ──
        if episodic_memory:
            try:
                episodic_memory.save_turn(clean_input, reply, tags=[brain])
            except Exception:
                pass

        yield {"type": "complete", "reply": reply, "brain": brain,
               "actions": serializable_actions, "duration_ms": duration_ms, "task_id": task.id}

    def _handle_slash_command(self, cmd: str) -> AgentResponse:
        """Handle built-in slash commands."""
        parts = cmd.split()
        command = parts[0].lower()
        args: List[str] = list(parts[1:]) if len(parts) > 1 else []

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
            try:
                from tools.system_info import SystemInfo
                si = SystemInfo()
                data = si.get_all()
                cpu = data.get('cpu', {})
                mem = data.get('memory', {})
                disk = data.get('disk', {})
                battery = data.get('battery')
                ollama_status = "🟢 Online" if (self.ollama and self.ollama.is_available()) else "🔴 Offline"
                gemini_status = "🟢 Online" if (self.gemini and self.gemini.is_available()) else "🔴 Offline"
                battery_str = "Desktop (no battery)"
                if battery and isinstance(battery, dict):
                    battery_str = f"{battery.get('percent', '?')}% ({'charging' if battery.get('plugged') else 'on battery'})"
                reply = f"""**System Status:**
• CPU: {cpu.get('percent', '?')}% ({cpu.get('cores', '?')} cores)
• RAM: {mem.get('used_gb', '?')}GB / {mem.get('total_gb', '?')}GB ({mem.get('percent', '?')}%)
• Disk: {disk.get('used_gb', '?')}GB / {disk.get('total_gb', '?')}GB ({disk.get('percent', '?')}%)
• Battery: {battery_str}

**AI Brains:**
• Ollama (Local): {ollama_status}
• Gemini: {gemini_status}
• Active Brain: {self._default_brain.upper()}"""
            except Exception as e:
                reply = f"Error getting status: {e}"

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
            try:
                from memory.preference_store import get_all_preferences
                prefs = get_all_preferences(db)
            except ImportError:
                prefs = {}
            db.close()
            if not prefs:
                reply = "No preferences stored yet."
            else:
                lines = ["**Stored Preferences:**"]
                for k, v in prefs.items():
                    lines.append(f"• {k}: {v}")
                reply = "\n".join(lines)

        elif command == "/briefing":
            try:
                from agent.briefing import daily_briefing
                briefing = asyncio.get_event_loop().run_until_complete(daily_briefing.generate())
                reply = daily_briefing.format_text(briefing)
            except Exception as e:
                reply = f"Briefing Error: {e}"

        else:
            reply = f"Unknown command: {cmd}\nType `/help` for available commands."

        return AgentResponse(reply=reply, brain="system", success=True)

    async def handle_voice_command(self, text: str):
        """Process a command received via voice."""
        print(f"🎤 Voice Command: {text}")
        
        try:
            # Reuse the full text processing pipeline (memory, routing, tools, logging)
            response: AgentResponse = await self.process(text)
            
            # Speak the text response
            if response.reply:
                # Remove emojis for cleaner speech if needed, or let engine handle it
                clean_reply = response.reply
                try:
                    from tools.voice_engine import voice_engine
                    if voice_engine:
                        await voice_engine.speak(clean_reply)
                except ImportError:
                    pass
                    
        except Exception as e:
            print(f"Voice Error: {e}")
            try:
                from tools.voice_engine import voice_engine
                if voice_engine:
                    await voice_engine.speak("I'm sorry, I encountered an error.")
            except ImportError:
                pass

    def set_default_brain(self, brain: str):
        self._default_brain = brain


# Singleton instance
orchestrator = AgentOrchestrator()
