"""
EONIX Memory Tool — Allows the AI to store long-term memories.
"""
from memory.semantic import SemanticMemory
from tools.tool_result import ToolResult

class MemoryTool:
    def __init__(self):
        self.memory = SemanticMemory()

    def store_fact(self, fact: str) -> ToolResult:
        """Store a fact in long-term memory."""
        try:
            fact_id = self.memory.store_fact(fact)
            return ToolResult(success=True, message=f"Fact stored in memory: '{fact}'", data={"id": fact_id})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to store fact: {str(e)}")
