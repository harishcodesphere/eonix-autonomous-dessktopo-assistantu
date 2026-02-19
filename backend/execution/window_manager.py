"""
Eonix Window Manager
List, arrange, resize, and manage desktop windows.
"""
from loguru import logger

try:
    import pygetwindow as gw
    PYGETWINDOW_AVAILABLE = True
except ImportError:
    PYGETWINDOW_AVAILABLE = False
    logger.warning("pygetwindow not installed. Window management disabled.")


class WindowManager:
    """Manages desktop window positions and states."""

    async def list_windows(self) -> list[dict]:
        """List all visible windows."""
        if not PYGETWINDOW_AVAILABLE:
            return []
        try:
            windows = gw.getAllWindows()
            return [
                {
                    "title": w.title,
                    "left": w.left,
                    "top": w.top,
                    "width": w.width,
                    "height": w.height,
                    "visible": w.visible,
                    "minimized": w.isMinimized,
                    "maximized": w.isMaximized,
                }
                for w in windows
                if w.title.strip()
            ]
        except Exception as e:
            logger.error(f"Failed to list windows: {e}")
            return []

    async def arrange_split(self, left_title: str, right_title: str) -> dict:
        """Arrange two windows side by side."""
        if not PYGETWINDOW_AVAILABLE:
            return {"status": "error", "message": "pygetwindow not available"}

        try:
            import ctypes
            user32 = ctypes.windll.user32
            screen_w = user32.GetSystemMetrics(0)
            screen_h = user32.GetSystemMetrics(1)

            left_wins = gw.getWindowsWithTitle(left_title)
            right_wins = gw.getWindowsWithTitle(right_title)

            if left_wins:
                left_wins[0].restore()
                left_wins[0].moveTo(0, 0)
                left_wins[0].resizeTo(screen_w // 2, screen_h)
            if right_wins:
                right_wins[0].restore()
                right_wins[0].moveTo(screen_w // 2, 0)
                right_wins[0].resizeTo(screen_w // 2, screen_h)

            return {"status": "success", "message": f"Arranged {left_title} and {right_title} side by side"}
        except Exception as e:
            logger.error(f"Failed to arrange windows: {e}")
            return {"status": "error", "message": str(e)}

    async def minimize_all(self) -> dict:
        """Minimize all windows."""
        if not PYGETWINDOW_AVAILABLE:
            return {"status": "error", "message": "pygetwindow not available"}
        try:
            for w in gw.getAllWindows():
                if w.title.strip() and w.visible:
                    w.minimize()
            return {"status": "success", "message": "All windows minimized"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def focus_window(self, title: str) -> dict:
        """Bring a window to focus."""
        if not PYGETWINDOW_AVAILABLE:
            return {"status": "error", "message": "pygetwindow not available"}
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                windows[0].activate()
                return {"status": "success", "message": f"Focused: {title}"}
            return {"status": "error", "message": f"Window not found: {title}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
