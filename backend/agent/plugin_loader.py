"""
EONIX Plugin System — Hot-loadable plugins for extensibility.
Plugins are Python modules placed in backend/plugins/ directory.
Each plugin must have a `register(tools: ToolRegistry)` function.
"""
import os
import importlib
import importlib.util
import sys
from typing import Any, Dict, List, Optional, Tuple

PLUGINS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")

class PluginLoader:
    """Load and manage EONIX plugins."""

    def __init__(self):
        self.loaded_plugins = {}
        os.makedirs(PLUGINS_DIR, exist_ok=True)

    def discover(self) -> List[str]:
        """Find all plugin files in the plugins directory."""
        plugins: List[str] = []
        if not os.path.exists(PLUGINS_DIR):
            return plugins
        for filename in os.listdir(PLUGINS_DIR):
            if filename.endswith('.py') and not filename.startswith('_'):
                name, _ext = os.path.splitext(filename)
                plugins.append(name)
        return plugins

    def load_all(self, tool_registry: Any = None) -> Dict[str, Dict[str, Any]]:
        """Load all discovered plugins."""
        results: Dict[str, Dict[str, Any]] = {}
        for plugin_name in self.discover():
            success, msg = self.load(plugin_name, tool_registry)
            results[plugin_name] = {"success": success, "message": msg}
        return results

    def load(self, plugin_name: str, tool_registry: Any = None) -> Tuple[bool, str]:
        """Load a single plugin by name."""
        try:
            plugin_path = os.path.join(PLUGINS_DIR, f"{plugin_name}.py")
            if not os.path.exists(plugin_path):
                return False, f"Plugin file not found: {plugin_name}.py"

            spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", plugin_path)
            if spec is None:
                return False, f"Could not load spec for plugin: {plugin_name}"
            loader = spec.loader
            if loader is None:
                return False, f"No loader found for plugin: {plugin_name}"
            module = importlib.util.module_from_spec(spec)
            loader.exec_module(module)

            # Call register() if it exists
            if hasattr(module, 'register') and tool_registry:
                module.register(tool_registry)

            self.loaded_plugins[plugin_name] = module
            return True, f"Plugin '{plugin_name}' loaded successfully"
        except Exception as e:
            return False, f"Plugin '{plugin_name}' failed: {str(e)}"

    def get_info(self) -> List[Dict[str, str]]:
        """Get info about loaded plugins."""
        info: List[Dict[str, str]] = []
        for name, module in self.loaded_plugins.items():
            info.append({
                "name": name,
                "description": getattr(module, '__doc__', 'No description') or 'No description',
                "version": getattr(module, '__version__', '1.0'),
            })
        return info


# Global instance
plugin_loader = PluginLoader()
