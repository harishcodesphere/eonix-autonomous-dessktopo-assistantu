"""
EONIX Plugin System — Hot-loadable plugins for extensibility.
Plugins are Python modules placed in backend/plugins/ directory.
Each plugin must have a `register(tools: ToolRegistry)` function.
"""
import os
import importlib
import importlib.util
import sys

PLUGINS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")

class PluginLoader:
    """Load and manage EONIX plugins."""

    def __init__(self):
        self.loaded_plugins = {}
        os.makedirs(PLUGINS_DIR, exist_ok=True)

    def discover(self) -> list:
        """Find all plugin files in the plugins directory."""
        plugins = []
        if not os.path.exists(PLUGINS_DIR):
            return plugins
        for filename in os.listdir(PLUGINS_DIR):
            if filename.endswith('.py') and not filename.startswith('_'):
                plugins.append(filename[:-3])  # Remove .py
        return plugins

    def load_all(self, tool_registry=None) -> dict:
        """Load all discovered plugins."""
        results = {}
        for plugin_name in self.discover():
            success, msg = self.load(plugin_name, tool_registry)
            results[plugin_name] = {"success": success, "message": msg}
        return results

    def load(self, plugin_name: str, tool_registry=None) -> tuple:
        """Load a single plugin by name."""
        try:
            plugin_path = os.path.join(PLUGINS_DIR, f"{plugin_name}.py")
            if not os.path.exists(plugin_path):
                return False, f"Plugin file not found: {plugin_name}.py"

            spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Call register() if it exists
            if hasattr(module, 'register') and tool_registry:
                module.register(tool_registry)

            self.loaded_plugins[plugin_name] = module
            return True, f"Plugin '{plugin_name}' loaded successfully"
        except Exception as e:
            return False, f"Plugin '{plugin_name}' failed: {str(e)}"

    def get_info(self) -> list:
        """Get info about loaded plugins."""
        info = []
        for name, module in self.loaded_plugins.items():
            info.append({
                "name": name,
                "description": getattr(module, '__doc__', 'No description') or 'No description',
                "version": getattr(module, '__version__', '1.0'),
            })
        return info


# Global instance
plugin_loader = PluginLoader()
