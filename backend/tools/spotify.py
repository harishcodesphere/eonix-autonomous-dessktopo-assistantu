"""
EONIX Spotify / Music Control — Media key shortcuts + browser fallback.
"""
import subprocess
import time
import pyautogui
from tools.tool_result import ToolResult


class SpotifyTool:
    name = "spotify_control"
    description = "Control music playback (play, pause, next, previous) or search Spotify"

    def execute(self, action: str = "play_pause", query: str = "", **_) -> ToolResult:
        action = action.lower().strip()

        if action in ("play", "pause", "play_pause", "toggle"):
            return self._media_key("playpause")
        elif action in ("next", "skip"):
            return self._media_key("nexttrack")
        elif action in ("previous", "prev", "back"):
            return self._media_key("prevtrack")
        elif action in ("volume_up", "louder"):
            return self._media_key("volumeup")
        elif action in ("volume_down", "quieter", "softer"):
            return self._media_key("volumedown")
        elif action in ("mute", "unmute"):
            return self._media_key("volumemute")
        elif action == "search" and query:
            return self._search_spotify(query)
        elif action == "open":
            return self._open_spotify()
        else:
            return ToolResult(success=False, message=f"Unknown action: {action}. Use: play, pause, next, prev, search, open")

    def _media_key(self, key: str) -> ToolResult:
        """Press a media key."""
        try:
            pyautogui.press(key)
            labels = {
                "playpause": "⏯ Toggled play/pause",
                "nexttrack": "⏭ Skipped to next track",
                "prevtrack": "⏮ Back to previous track",
                "volumeup": "🔊 Volume up",
                "volumedown": "🔉 Volume down",
                "volumemute": "🔇 Toggled mute",
            }
            return ToolResult(success=True, message=labels.get(key, f"Pressed {key}"))
        except Exception as e:
            return ToolResult(success=False, message=f"Media key failed: {e}")

    def _open_spotify(self) -> ToolResult:
        """Open Spotify desktop app."""
        try:
            subprocess.Popen(["spotify.exe"], shell=True)
            return ToolResult(success=True, message="🎵 Opening Spotify...")
        except Exception:
            # Fallback: open web version
            import webbrowser
            webbrowser.open("https://open.spotify.com")
            return ToolResult(success=True, message="🎵 Opening Spotify Web Player...")

    def _search_spotify(self, query: str) -> ToolResult:
        """Open Spotify search in browser."""
        import webbrowser
        url = f"https://open.spotify.com/search/{query}"
        webbrowser.open(url)
        return ToolResult(success=True, message=f"🎵 Searching Spotify for '{query}'...")
