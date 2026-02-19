"""
Eonix Plugin Manager
Manages the full lifecycle of plugins: install, enable, disable, list.
"""
import os
import importlib
import sys
from typing import Dict, Any, List
from loguru import logger
from plugins.base import PluginBase


class PluginManager:
    """Manages plugin discovery, loading, and execution."""

    def __init__(self, builtin_dir: str = None, user_dir: str = None):
        self.builtin_dir = builtin_dir or os.path.join(os.path.dirname(__file__), "builtin")
        self.user_dir = user_dir
        self.plugins: Dict[str, PluginBase] = {}

    async def load_all(self):
        """Load all built-in and user plugins."""
        await self._load_from_dir(self.builtin_dir, "builtin")
        if self.user_dir and os.path.exists(self.user_dir):
            await self._load_from_dir(self.user_dir, "user")
        logger.info(f"Loaded {len(self.plugins)} plugins")

    async def _load_from_dir(self, directory: str, source: str):
        """Load plugins from a directory."""
        if not os.path.exists(directory):
            return

        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                try:
                    # Add dir to path if needed
                    if directory not in sys.path:
                        sys.path.insert(0, directory)

                    spec = importlib.util.spec_from_file_location(
                        module_name,
                        os.path.join(directory, filename),
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Look for a Plugin class
                    plugin_class = getattr(module, "Plugin", None)
                    if plugin_class and issubclass(plugin_class, PluginBase):
                        instance = plugin_class()
                        await instance.initialize()
                        self.plugins[module_name] = instance
                        logger.info(f"Loaded {source} plugin: {instance.name}")
                    elif plugin_class:
                        # Legacy plugins without PluginBase
                        instance = plugin_class()
                        if hasattr(instance, "initialize"):
                            await instance.initialize()
                        self.plugins[module_name] = instance
                        logger.info(f"Loaded {source} plugin (legacy): {module_name}")

                except Exception as e:
                    logger.error(f"Failed to load plugin {module_name}: {e}")

    async def execute_plugin(self, plugin_name: str, action: str, params: dict = None) -> Any:
        """Execute an action on a specific plugin."""
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            return {"status": "error", "message": f"Plugin '{plugin_name}' not found"}

        if hasattr(plugin, "enabled") and not plugin.enabled:
            return {"status": "error", "message": f"Plugin '{plugin_name}' is disabled"}

        try:
            result = await plugin.execute(action, params or {})
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Plugin {plugin_name} action {action} failed: {e}")
            return {"status": "error", "message": str(e)}

    def enable_plugin(self, name: str) -> bool:
        if name in self.plugins and hasattr(self.plugins[name], "enabled"):
            self.plugins[name].enabled = True
            return True
        return False

    def disable_plugin(self, name: str) -> bool:
        if name in self.plugins and hasattr(self.plugins[name], "enabled"):
            self.plugins[name].enabled = False
            return True
        return False

    def list_plugins(self) -> List[Dict]:
        """List all loaded plugins."""
        return [
            {
                "name": getattr(p, "name", key),
                "description": getattr(p, "description", ""),
                "version": getattr(p, "version", "unknown"),
                "enabled": getattr(p, "enabled", True),
                "key": key,
            }
            for key, p in self.plugins.items()
        ]

    async def shutdown_all(self):
        """Shutdown all plugins."""
        for name, plugin in self.plugins.items():
            try:
                if hasattr(plugin, "shutdown"):
                    await plugin.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down plugin {name}: {e}")
