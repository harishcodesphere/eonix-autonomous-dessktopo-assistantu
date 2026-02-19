"""
EONIX App Usage Tracker — Background daemon that polls the active window
every 30 seconds and records usage sessions in SQLite.
"""
import threading
import time
import os
from datetime import datetime

# Windows-specific imports (optional-safe)
try:
    import win32gui
    import win32process
    import psutil
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

from memory.db import SessionLocal, AppUsage

# ── Productive app classification ──────────────────────────────
PRODUCTIVE_APPS = {
    "code", "visual studio code", "pycharm", "intellij", "webstorm",
    "sublime text", "notepad++", "terminal", "cmd", "powershell",
    "windows terminal", "git", "postman", "figma", "adobe",
    "word", "excel", "powerpoint", "notion", "obsidian",
    "jupyter", "anaconda", "python", "node",
}

DISTRACTION_APPS = {
    "chrome", "firefox", "edge", "brave",  # browsing (grey area)
    "youtube", "netflix", "twitch", "discord", "telegram",
    "instagram", "twitter", "reddit", "tiktok",
    "spotify", "vlc", "media player",
    "steam", "epic games", "minecraft",
}


def classify_app(app_name: str) -> str:
    """Return 'productive', 'distraction', or 'neutral'."""
    lower = app_name.lower()
    for p in PRODUCTIVE_APPS:
        if p in lower:
            return "productive"
    for d in DISTRACTION_APPS:
        if d in lower:
            return "distraction"
    return "neutral"


def _get_active_window_info() -> dict:
    """Get the currently focused window's app name and title."""
    if not HAS_WIN32:
        return {"app": "Unknown", "title": "Unknown"}
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        app = proc.name().replace(".exe", "").strip()
        return {"app": app, "title": title}
    except Exception:
        return {"app": "Unknown", "title": "Unknown"}


class UsageTracker:
    """Background daemon that samples the active window every INTERVAL seconds."""

    INTERVAL = 30  # seconds

    def __init__(self):
        self._thread = None
        self._running = False
        self._current_app = None
        self._current_title = None
        self._session_start = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True, name="UsageTracker")
        self._thread.start()

    def stop(self):
        self._running = False
        # Finalize any open session
        self._end_session()

    # ── Core loop ──────────────────────────────────────────────
    def _loop(self):
        while self._running:
            try:
                info = _get_active_window_info()
                app = info["app"]
                title = info["title"]

                if app != self._current_app:
                    # App changed → end old session, start new one
                    self._end_session()
                    self._current_app = app
                    self._current_title = title
                    self._session_start = datetime.now()
                else:
                    # Same app — update title if changed
                    self._current_title = title

            except Exception as e:
                print(f"[UsageTracker] poll error: {e}")

            time.sleep(self.INTERVAL)

    def _end_session(self):
        """Write the completed session to DB."""
        if not self._current_app or not self._session_start:
            return
        try:
            now = datetime.now()
            duration = (now - self._session_start).total_seconds()
            if duration < 2:
                return  # skip sub-2-second flickers

            db = SessionLocal()
            row = AppUsage(
                app_name=self._current_app,
                window_title=self._current_title or "",
                start_time=self._session_start,
                end_time=now,
                duration_seconds=round(duration, 1),
                date=self._session_start.strftime("%Y-%m-%d"),
            )
            db.add(row)
            db.commit()
            db.close()
        except Exception as e:
            print(f"[UsageTracker] save error: {e}")
        finally:
            self._current_app = None
            self._current_title = None
            self._session_start = None


# Singleton
usage_tracker = UsageTracker()
