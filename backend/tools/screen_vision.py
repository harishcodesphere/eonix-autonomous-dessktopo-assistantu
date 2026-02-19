"""
EONIX Screen Vision — See and understand the screen using pyautogui, OCR, and Gemini Vision.
"""
import os
import time
import json
import base64
import pyautogui
from typing import Dict, Any, Optional

try:
    import pytesseract
    from PIL import Image
    # Set tesseract path if needed, usually cleaner to let user set it in PATH
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("WARNING: pytesseract not found. OCR features will be limited.")

try:
    # Try relative import first (when running as package)
    from ..brains.gemini_brain import GeminiBrain
except (ImportError, ValueError):
    try:
        # Try absolute import (when running from root)
        from brains.gemini_brain import GeminiBrain
    except ImportError:
        GeminiBrain = None

class ScreenVision:
    def __init__(self):
        self.gemini = GeminiBrain() if GeminiBrain else None
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def take_screenshot(self, filename: str = "latest.png") -> str:
        """Capture the current screen and save to disk."""
        path = os.path.join(self.screenshot_dir, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return path

    def read_screen(self, question: str) -> str:
        """Capture screen and ask Gemini what it sees."""
        if not self.gemini or not self.gemini.is_available():
            return "Vision AI (Gemini) is not available."
        
        path = self.take_screenshot(f"query_{int(time.time())}.png")
        
        # We need to run async gemini method from sync tool context
        # This is tricky because tools are run in a thread pool.
        # We'll use a helper or simple run_until_complete if possible, 
        # but since we are already in a thread, we can use new event loop.
        import asyncio
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            answer = loop.run_until_complete(self.gemini.analyze_screen(path, question))
            loop.close()
            return answer
        except Exception as e:
            return f"Vision Error: {e}"

    def extract_screen_text(self) -> str:
        """Get all text from the screen using OCR."""
        if not OCR_AVAILABLE:
            return "OCR library (pytesseract) is not installed."
        
        try:
            path = self.take_screenshot("ocr.png")
            text = pytesseract.image_to_string(Image.open(path))
            return text.strip()
        except Exception as e:
            return f"OCR Error: {e} (Do you have Tesseract installed in PATH?)"

    def find_on_screen(self, element_description: str) -> Dict[str, Any]:
        """
        Ask Gemini to find coordinates of an element.
        Returns: {"x": 100, "y": 200, "confidence": 0.9}
        """
        if not self.gemini or not self.gemini.is_available():
            return {"error": "Vision AI unavailable"}

        path = self.take_screenshot("find.png")
        
        prompt = f"""
        I need to click on '{element_description}'.
        Return a JSON object with the center x, y coordinates of this element.
        Format: {{"x": 123, "y": 456, "confidence": 0.9}}
        If not found, return {{"error": "not found"}}.
        IMAGE SIZE: {pyautogui.size()}
        """
        
        import asyncio
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # We reuse analyze_screen but context is JSON request
            resp_text = loop.run_until_complete(self.gemini.analyze_screen(path, prompt))
            loop.close()
            
            # Parse JSON
            import re
            match = re.search(r'\{.*\}', resp_text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"error": "Could not parse coordinates", "raw": resp_text}
            
        except Exception as e:
            return {"error": str(e)}

    def click_element(self, description: str) -> str:
        """Find an element by description and click it."""
        coords = self.find_on_screen(description)
        if "error" in coords:
            return f"Could not find '{description}': {coords['error']}"
        
        x = coords.get("x")
        y = coords.get("y")
        
        if x and y:
            pyautogui.moveTo(x, y, duration=1.0) # Move slowly to show user
            pyautogui.click()
            return f"Clicked '{description}' at ({x}, {y})"
        
        return "Invalid coordinates returned."
