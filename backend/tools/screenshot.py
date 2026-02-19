"""
EONIX Screenshot — Screen capture tool.
"""
import os
import time
from datetime import datetime
from .tool_result import ToolResult


class Screenshot:
    name = "take_screenshot"
    description = "Takes a screenshot of the current screen"

    SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "screenshots")

    def execute(self, filename: str = None) -> ToolResult:
        """Take a screenshot and save it."""
        try:
            import pyautogui
            os.makedirs(self.SAVE_DIR, exist_ok=True)
            if not filename:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(self.SAVE_DIR, filename)
            time.sleep(0.5)  # Brief pause to let UI settle
            img = pyautogui.screenshot()
            img.save(path)
            return ToolResult(
                success=True,
                message=f"Screenshot saved: {filename}",
                data={"path": path, "filename": filename}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Screenshot failed: {str(e)}")
