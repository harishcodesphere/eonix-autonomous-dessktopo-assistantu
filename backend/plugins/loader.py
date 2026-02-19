import importlib
import os
import sys
from typing import Dict, Any
from loguru import logger

class PluginBase:
    def __init__(self, name: str):
        self.name = name

    async def initialize(self):
        pass

    async def execute(self, action: str, params: dict) -> Any:
        pass

class PluginLoader:
    def __init__(self, plugin_dir: str):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, PluginBase] = {}
        if self.plugin_dir not in sys.path:
            sys.path.append(self.plugin_dir)

    async def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir, exist_ok=True)
            return

        for folder in os.listdir(self.plugin_dir):
            folder_path = os.path.join(self.plugin_dir, folder)
            if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, "__init__.py")):
                try:
                    module = importlib.import_module(folder)
                    if hasattr(module, "Plugin"):
                        plugin_instance = module.Plugin()
                        await plugin_instance.initialize()
                        self.plugins[folder] = plugin_instance
                        logger.info(f"Loaded plugin: {folder}")
                except Exception as e:
                    logger.error(f"Failed to load plugin {folder}: {e}")

    def get_plugin(self, name: str) -> PluginBase:
        return self.plugins.get(name)
