"""
Eonix Built-in Plugin: Browser Automation
Web automation using subprocess and browser controls.
"""
import subprocess
import webbrowser
from plugins.base import PluginBase
from loguru import logger


class BrowserAutomationPlugin(PluginBase):
    name = "Browser Automation"
    description = "Open URLs, search the web, and automate browser actions"
    version = "1.0.0"

    async def initialize(self):
        logger.info("Browser Automation plugin initialized")

    async def execute(self, action: str, params: dict):
        actions = {
            "open_url": self._open_url,
            "search": self._search,
            "open_tab": self._open_tab,
        }
        handler = actions.get(action)
        if handler:
            return await handler(params)
        return {"error": f"Unknown action: {action}"}

    async def _open_url(self, params: dict):
        url = params.get("url", "")
        if not url:
            return {"error": "No URL provided"}
        try:
            webbrowser.open(url)
            return {"status": "success", "message": f"Opened: {url}"}
        except Exception as e:
            return {"error": str(e)}

    async def _search(self, params: dict):
        query = params.get("query", "")
        if not query:
            return {"error": "No search query provided"}
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        try:
            webbrowser.open(url)
            return {"status": "success", "message": f"Searching: {query}"}
        except Exception as e:
            return {"error": str(e)}

    async def _open_tab(self, params: dict):
        url = params.get("url", "about:blank")
        try:
            webbrowser.open_new_tab(url)
            return {"status": "success", "message": f"New tab opened: {url}"}
        except Exception as e:
            return {"error": str(e)}

    def get_commands(self):
        return [
            {"name": "open_url", "description": "Open a URL in the browser"},
            {"name": "search", "description": "Search the web"},
            {"name": "open_tab", "description": "Open a new browser tab"},
        ]


Plugin = BrowserAutomationPlugin
