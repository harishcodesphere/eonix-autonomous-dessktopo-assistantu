"""
EONIX ToolResult — Standard return type for all tools.
"""
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ToolResult:
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        icon = "✓" if self.success else "✗"
        return f"{icon} {self.message}"
