"""
EONIX Typer — Keyboard control and text input automation.
Uses clipboard paste for reliability (handles unicode, spaces, special chars).
"""
import time
import pyperclip
import pyautogui
from .tool_result import ToolResult

# Safety: disable pyautogui failsafe for automation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05


class Typer:
    name = "type_text"
    description = "Types text into the currently focused window using clipboard paste"

    def execute(self, text: str, delay_before: float = 2.0, press_enter: bool = False) -> ToolResult:
        """Type text into the active window."""
        try:
            time.sleep(delay_before)
            # Use clipboard paste — most reliable method
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            if press_enter:
                pyautogui.press('enter')
            return ToolResult(success=True, message=f"Typed: {text[:50]}{'...' if len(text) > 50 else ''}")
        except Exception as e:
            # Fallback to typewrite
            try:
                time.sleep(0.3)
                pyautogui.typewrite(text, interval=0.04)
                if press_enter:
                    pyautogui.press('enter')
                return ToolResult(success=True, message=f"Typed (fallback): {text[:50]}")
            except Exception as e2:
                return ToolResult(success=False, message=f"Failed to type text: {str(e2)}")

    def press_keys(self, keys: str, delay_before: float = 0.3) -> ToolResult:
        """Press keyboard shortcuts like 'ctrl+s', 'alt+f4', 'enter', 'win+d'."""
        try:
            time.sleep(delay_before)
            # Parse key combination
            parts = [k.strip().lower() for k in keys.split('+')]
            if len(parts) == 1:
                pyautogui.press(parts[0])
            else:
                pyautogui.hotkey(*parts)
            return ToolResult(success=True, message=f"Pressed: {keys}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to press {keys}: {str(e)}")

    def select_all_and_type(self, text: str) -> ToolResult:
        """Select all existing text and replace with new text."""
        try:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            return self.execute(text, delay_before=0.2)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed: {str(e)}")

    def save_file(self) -> ToolResult:
        """Save the current file with Ctrl+S."""
        return self.press_keys('ctrl+s', delay_before=0.5)

    def copy_to_clipboard(self, text: str) -> ToolResult:
        """Copy text to clipboard."""
        try:
            pyperclip.copy(text)
            return ToolResult(success=True, message=f"Copied to clipboard: {text[:50]}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to copy: {str(e)}")
