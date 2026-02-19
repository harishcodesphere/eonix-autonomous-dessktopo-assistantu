"""
EONIX Browser Tool — Web browsing and search automation.
Uses webbrowser for simple tasks, playwright for advanced automation.
"""
import webbrowser
import urllib.parse
import time
from .tool_result import ToolResult


class BrowserTool:
    name = "browser_action"
    description = "Opens browser, navigates URLs, searches Google, YouTube, Maps"

    def search_google(self, query: str) -> ToolResult:
        """Search Google in the default browser."""
        try:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            return ToolResult(success=True, message=f"Searching Google for: {query}", data={"url": url})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to search: {str(e)}")

    def open_url(self, url: str) -> ToolResult:
        """Open a specific URL."""
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            webbrowser.open(url)
            return ToolResult(success=True, message=f"Opened: {url}", data={"url": url})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to open URL: {str(e)}")

    def search_youtube(self, query: str) -> ToolResult:
        """Search YouTube."""
        try:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)
            return ToolResult(success=True, message=f"Searching YouTube for: {query}", data={"url": url})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to search YouTube: {str(e)}")

    def open_gmail(self) -> ToolResult:
        """Open Gmail."""
        try:
            webbrowser.open("https://mail.google.com")
            return ToolResult(success=True, message="Opened Gmail")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to open Gmail: {str(e)}")

    def open_maps(self, location: str) -> ToolResult:
        """Open Google Maps for a location."""
        try:
            url = f"https://maps.google.com/?q={urllib.parse.quote(location)}"
            webbrowser.open(url)
            return ToolResult(success=True, message=f"Opened Maps for: {location}", data={"url": url})
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to open Maps: {str(e)}")

    def open_github(self, repo: str = "") -> ToolResult:
        """Open GitHub."""
        try:
            url = f"https://github.com/{repo}" if repo else "https://github.com"
            webbrowser.open(url)
            return ToolResult(success=True, message=f"Opened GitHub{': ' + repo if repo else ''}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed: {str(e)}")

    def execute(self, action: str, query: str = "", url: str = "") -> ToolResult:
        """Universal browser action dispatcher."""
        action = action.lower()
        if action == "search_google":
            return self.search_google(query)
        elif action == "open_url":
            return self.open_url(url or query)
        elif action == "search_youtube":
            return self.search_youtube(query)
        elif action == "open_gmail":
            return self.open_gmail()
        elif action == "open_maps":
            return self.open_maps(query)
        elif action == "open_github":
            return self.open_github(query)
        else:
            # Default: try to open as URL or search
            if query:
                return self.search_google(query)
            return self.open_url(url)
