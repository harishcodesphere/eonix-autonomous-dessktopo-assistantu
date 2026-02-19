"""
EONIX Smart Chatbot Engine — NLP-powered conversational AI.
Handles all types of questions with multi-turn context, personality,
and knowledge-augmented responses across every domain.
"""
import json
import time
from typing import List, Dict, Optional
from loguru import logger

from ai.ollama_client import OllamaClient
from ai.prompts import get_prompt
from agent.personality import PersonalityEngine


class ConversationMemory:
    """Maintains sliding window of conversation history for context."""

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._history: List[Dict[str, str]] = []

    def add(self, role: str, content: str):
        """Add a message to conversation history."""
        self._history.append({"role": role, "content": content})
        # Keep within sliding window
        if len(self._history) > self.max_turns * 2:
            self._history = self._history[-(self.max_turns * 2):]

    def get_messages(self) -> List[Dict[str, str]]:
        """Return conversation history in chat format."""
        return list(self._history)

    def get_context_summary(self) -> str:
        """Get a brief summary of recent conversation for context injection."""
        if not self._history:
            return ""
        recent = self._history[-6:]  # Last 3 exchanges
        lines = []
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Eonix"
            lines.append(f"{role}: {msg['content'][:150]}")
        return "Recent conversation:\n" + "\n".join(lines)

    def clear(self):
        """Clear conversation history."""
        self._history.clear()

    @property
    def turn_count(self) -> int:
        return len([m for m in self._history if m["role"] == "user"])


class Chatbot:
    """
    NLP-powered conversational chatbot engine for EONIX.
    Answers any question across all domains with personality and context.
    """

    def __init__(self):
        self.ollama = OllamaClient()
        self.personality = PersonalityEngine()
        self.memory = ConversationMemory(max_turns=20)
        self.system_prompt = get_prompt("chatbot")
        self._gemini = None

    def _get_gemini(self):
        """Lazy-load Gemini brain as fallback."""
        if self._gemini is None:
            try:
                from brains.gemini_brain import GeminiBrain
                brain = GeminiBrain()
                if brain.is_available():
                    self._gemini = brain
            except Exception:
                pass
        return self._gemini

    async def chat(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Process a chat message and return a rich conversational response.
        
        Returns: {
            "reply": str,
            "brain": str,
            "mood": str,
            "context_turns": int,
            "duration_ms": int
        }
        """
        start = time.time()

        # Detect mood for personality adaptation
        mood = self.personality.detect_mood(user_message)
        tone = self.personality.get_tone_instruction(mood)
        time_ctx = self.personality.get_time_context()

        # Add user message to memory
        self.memory.add("user", user_message)

        # Build conversation messages for the LLM
        messages = self._build_messages(user_message, conversation_history, mood, tone, time_ctx)

        # Try Ollama first (local, fast)
        reply = await self._try_ollama(messages)
        brain = "local"

        # If Ollama fails, try Gemini
        if self._is_error_response(reply):
            gemini = self._get_gemini()
            if gemini:
                try:
                    reply = gemini.chat(user_message)
                    brain = "gemini"
                except Exception as e:
                    logger.error(f"Gemini fallback failed: {e}")

        # If both fail, use built-in fallback
        if self._is_error_response(reply):
            reply = self._builtin_fallback(user_message, mood)
            brain = "fallback"

        # Clean up the response
        reply = self._clean_response(reply)

        # Add assistant response to memory
        self.memory.add("assistant", reply)

        duration_ms = int((time.time() - start) * 1000)

        return {
            "reply": reply,
            "brain": brain,
            "mood": mood,
            "context_turns": self.memory.turn_count,
            "duration_ms": duration_ms
        }

    def _build_messages(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]],
        mood: str,
        tone: str,
        time_ctx: str
    ) -> List[Dict[str, str]]:
        """Build the full message list for the LLM with context."""
        # System prompt with personality injection
        system = self.system_prompt + f"\n\n[Current mood: {mood}. {tone}. {time_ctx}]"

        messages = [{"role": "system", "content": system}]

        # Use provided conversation history OR internal memory
        if conversation_history and len(conversation_history) > 0:
            # Use the frontend-provided history (last 20 messages)
            for msg in conversation_history[-20:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})
        else:
            # Use internal memory
            for msg in self.memory.get_messages()[:-1]:  # Exclude current message (added above)
                messages.append(msg)

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    async def _try_ollama(self, messages: List[Dict[str, str]]) -> str:
        """Try to get a response from Ollama."""
        try:
            # Use chat endpoint for multi-turn conversation
            response = await self.ollama.chat(
                messages=messages[1:],  # Exclude system (passed separately)
                system_prompt=messages[0]["content"]
            )
            return response
        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            return f"❌ Error: {str(e)}"

    def _is_error_response(self, reply: str) -> bool:
        """Check if response indicates an error."""
        if not reply:
            return True
        error_markers = ["❌", "Error:", "error:", "not available", "not reachable", "Offline"]
        return any(marker in reply for marker in error_markers)

    def _clean_response(self, reply: str) -> str:
        """Clean up the LLM response."""
        if not reply:
            return "I'm here! How can I help you?"

        reply = reply.strip()

        # Remove markdown JSON wrappers if the LLM accidentally returns JSON
        if reply.startswith("```"):
            lines = reply.split("\n")
            if len(lines) > 2:
                reply = "\n".join(lines[1:-1])

        # Try to extract just the response if LLM returned JSON
        try:
            data = json.loads(reply)
            if isinstance(data, dict) and "response" in data:
                return data["response"]
        except (json.JSONDecodeError, TypeError):
            pass

        return reply

    def _builtin_fallback(self, user_message: str, mood: str) -> str:
        """Built-in responses when both LLMs are unavailable."""
        text = user_message.lower().strip()
        prefix = self.personality.get_mood_prefix(mood)

        # Knowledge-based fallback for common questions
        if any(w in text for w in ["hello", "hi ", "hey", "greetings"]):
            return f"{prefix}Hey there! I'm Eonix, your desktop assistant. How can I help you today?"

        if "who are you" in text or "what are you" in text:
            return (f"{prefix}I'm Eonix — your autonomous desktop assistant, inspired by JARVIS. "
                    "I can open apps, manage files, search the web, answer questions, and automate "
                    "tasks on your computer. Just ask me anything!")

        if any(w in text for w in ["thank", "thanks"]):
            return f"{prefix}You're welcome! Always happy to help. 😊"

        if any(w in text for w in ["how are you", "how r u"]):
            return f"{prefix}I'm running great! All systems operational. What can I do for you?"

        if "weather" in text:
            return (f"{prefix}I can't check live weather right now since I'm running offline, "
                    "but I can search it for you! Just say 'search weather in [your city]'.")

        if any(w in text for w in ["joke", "funny"]):
            return (f"{prefix}Why do programmers prefer dark mode? "
                    "Because light attracts bugs! 🐛😄")

        if any(w in text for w in ["time", "date"]):
            from datetime import datetime
            now = datetime.now()
            return f"{prefix}It's {now.strftime('%I:%M %p')} on {now.strftime('%B %d, %Y')}."

        return (f"{prefix}I'd love to help with that, but my AI brain seems to be offline right now. "
                "Please make sure Ollama is running (`ollama serve`) and try again. "
                "Meanwhile, I can still execute commands like opening apps and managing files!")

    def reset_conversation(self):
        """Clear conversation history for a fresh start."""
        self.memory.clear()

    def get_conversation_stats(self) -> Dict:
        """Get conversation statistics."""
        return {
            "total_turns": self.memory.turn_count,
            "messages": len(self.memory.get_messages()),
            "current_mood": self.personality.current_mood,
        }


# Singleton instance
chatbot = Chatbot()
