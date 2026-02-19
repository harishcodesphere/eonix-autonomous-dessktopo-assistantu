"""
Eonix Application Controller
Launch, close, and manage desktop applications.
"""
import subprocess
import platform
from loguru import logger

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False


class AppController:
    """Controls desktop application lifecycle."""

    # Common application mappings (name -> executable)
    APP_MAP = {
        "chrome": "chrome",
        "firefox": "firefox",
        "vscode": "code",
        "visual studio code": "code",
        "notepad": "notepad",
        "calculator": "calc",
        "explorer": "explorer",
        "terminal": "cmd",
        "powershell": "powershell",
        "spotify": "spotify",
        "discord": "discord",
        "slack": "slack",
    }

    async def launch(self, app_name: str, args: list[str] = None) -> dict:
        """Launch an application."""
        executable = self.APP_MAP.get(app_name.lower(), app_name)
        try:
            cmd = [executable] + (args or [])
            if platform.system() == "Windows":
                subprocess.Popen(cmd, shell=True)
            else:
                subprocess.Popen(cmd)
            logger.info(f"Launched: {app_name} ({executable})")
            return {"status": "success", "message": f"Launched {app_name}"}
        except Exception as e:
            logger.error(f"Failed to launch {app_name}: {e}")
            return {"status": "error", "message": str(e)}

    async def close(self, app_name: str) -> dict:
        """Close an application by name."""
        if not PYGETWINDOW_AVAILABLE:
            return {"status": "error", "message": "pygetwindow not available"}
        try:
            windows = gw.getWindowsWithTitle(app_name)
            closed = 0
            for win in windows:
                win.close()
                closed += 1
            logger.info(f"Closed {closed} window(s) for: {app_name}")
            return {"status": "success", "message": f"Closed {closed} window(s) of {app_name}"}
        except Exception as e:
            logger.error(f"Failed to close {app_name}: {e}")
            return {"status": "error", "message": str(e)}

    async def focus(self, app_name: str) -> dict:
        """Bring an application to focus."""
        if not PYGETWINDOW_AVAILABLE:
            return {"status": "error", "message": "pygetwindow not available"}
        try:
            windows = gw.getWindowsWithTitle(app_name)
            if windows:
                windows[0].activate()
                return {"status": "success", "message": f"Focused on {app_name}"}
            return {"status": "error", "message": f"No window found for {app_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def list_running(self) -> list[dict]:
        """List all open windows."""
        if not PYGETWINDOW_AVAILABLE:
            return []
        try:
            windows = gw.getAllWindows()
            return [
                {"title": w.title, "visible": w.visible, "minimized": w.isMinimized}
                for w in windows if w.title.strip()
            ]
        except Exception:
            return []
