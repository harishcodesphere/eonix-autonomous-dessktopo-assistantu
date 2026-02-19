"""
Eonix Context Manager
Maintains conversation history and retrieves relevant context for AI calls.
"""
from typing import Optional
from loguru import logger


class ContextManager:
    """Manages conversation context and history for multi-turn interactions."""

    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.history: list[dict] = []
        self.session_data: dict = {}

    def add_interaction(self, user_input: str, response: str, intent: dict = None):
        """Add an interaction to conversation history."""
        entry = {
            "user_input": user_input,
            "response": response,
            "intent": intent,
        }
        self.history.append(entry)

        # Trim to max_history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    async def get_context(self, current_input: str, intent: dict = None) -> dict:
        """
        Build context for the current request.
        Includes recent history, session data, and inferred references.
        """
        recent = self.history[-5:] if self.history else []

        context = {
            "recent_history": recent,
            "session_data": self.session_data,
            "turn_count": len(self.history),
        }

        # Check if user references a previous interaction ("it", "that", "them")
        if self._has_back_reference(current_input):
            context["back_reference"] = self.history[-1] if self.history else None

        return context

    def set_session_data(self, key: str, value):
        """Store session-level data (e.g., current working directory, active project)."""
        self.session_data[key] = value

    def get_session_data(self, key: str, default=None):
        return self.session_data.get(key, default)

    def clear(self):
        """Clear all context."""
        self.history.clear()
        self.session_data.clear()

    def get_conversation_summary(self) -> str:
        """Generate a summary of the conversation so far."""
        if not self.history:
            return "No previous interactions."
        lines = []
        for entry in self.history[-5:]:
            lines.append(f"User: {entry['user_input']}")
            lines.append(f"Eonix: {entry['response'][:100]}...")
        return "\n".join(lines)

    @staticmethod
    def _has_back_reference(text: str) -> bool:
        """Detect if user input references a previous result."""
        back_refs = ["it", "that", "them", "those", "the same", "again", "also"]
        words = text.lower().split()
        return any(ref in words for ref in back_refs)
