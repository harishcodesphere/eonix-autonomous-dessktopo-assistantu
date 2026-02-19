import asyncio
from typing import List, Dict, Callable
from loguru import logger
import pyautogui

class AutomationEngine:
    def __init__(self):
        self.workflows: Dict[str, List[Dict]] = {}
        self.running = False
        # Fail-safe: moving mouse to corner will abort
        pyautogui.FAILSAFE = True

    async def type_text(self, text: str, interval: float = 0.05):
        """Simulate typing text."""
        try:
            logger.info(f"Typing: {text}")
            pyautogui.write(text, interval=interval)
            return {"status": "success", "message": f"Typed: {text}"}
        except Exception as e:
            logger.error(f"Typing failed: {e}")
            return {"status": "error", "message": str(e)}

    async def press_key(self, key: str):
        """Simulate key press."""
        try:
            pyautogui.press(key)
            return {"status": "success", "message": f"Pressed: {key}"}
        except Exception as e:
            logger.error(f"Key press failed: {e}")
            return {"status": "error", "message": str(e)}

    async def execute_automation(self, action: str, params: dict):
        """Execute a single automation action."""
        if action == "type":
            return await self.type_text(params.get("text", ""))
        elif action == "press":
            return await self.press_key(params.get("key", ""))
        return {"status": "error", "message": f"Unknown automation action: {action}"}

