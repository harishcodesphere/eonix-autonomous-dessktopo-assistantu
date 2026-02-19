"""
Eonix Plugin Base Class
All plugins must extend this base class.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class PluginBase(ABC):
    """Abstract base class for all Eonix plugins."""

    name: str = "Unnamed Plugin"
    description: str = ""
    version: str = "1.0.0"
    author: str = "Eonix"

    def __init__(self):
        self._enabled = True
        self._config: Dict = {}

    @abstractmethod
    async def initialize(self):
        """Called when the plugin is loaded."""
        pass

    @abstractmethod
    async def execute(self, action: str, params: dict) -> Any:
        """Execute a plugin action."""
        pass

    async def shutdown(self):
        """Called when the plugin is unloaded."""
        pass

    def get_commands(self) -> List[Dict]:
        """Return list of commands this plugin provides."""
        return []

    def configure(self, config: dict):
        """Apply configuration to the plugin."""
        self._config = config

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    def __repr__(self):
        return f"<Plugin: {self.name} v{self.version}>"
