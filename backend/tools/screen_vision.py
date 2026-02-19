"""
EONIX Screen Vision — AI-powered screen analysis.
Takes a screenshot and sends it to Gemini Vision for understanding.
"""
import os
import time
from datetime import datetime
from .tool_result import ToolResult

class ScreenVision:
    """Capture screen and analyze with AI vision."""

    SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "screenshots")

    def analyze(self, question: str = "What is on my screen?") -> ToolResult:
        """Take a screenshot and analyze it with Gemini Vision."""
        try:
            import pyautogui
            from brains.gemini_brain import GeminiBrain

            os.makedirs(self.SAVE_DIR, exist_ok=True)
            filename = f"vision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(self.SAVE_DIR, filename)

            time.sleep(0.3)
            img = pyautogui.screenshot()
            img.save(path)

            # Analyze with Gemini Vision
            gemini = GeminiBrain()
            if not gemini.is_available():
                return ToolResult(
                    success=False,
                    message="Gemini Vision is not available. Check API key."
                )

            analysis = gemini.analyze_screen(path, question)
            return ToolResult(
                success=True,
                message=analysis,
                data={"screenshot": path, "question": question, "analysis": analysis}
            )
        except Exception as e:
            return ToolResult(success=False, message=f"Screen vision failed: {str(e)}")

    def ocr_screen(self) -> ToolResult:
        """Extract text from screen using basic OCR (pytesseract fallback)."""
        try:
            import pyautogui
            os.makedirs(self.SAVE_DIR, exist_ok=True)
            path = os.path.join(self.SAVE_DIR, "ocr_temp.png")
            img = pyautogui.screenshot()
            img.save(path)

            try:
                import pytesseract
                text = pytesseract.image_to_string(img)
                return ToolResult(success=True, message=f"Extracted text:\n{text}", data={"text": text})
            except ImportError:
                # Fallback: use Gemini to read text
                from brains.gemini_brain import GeminiBrain
                gemini = GeminiBrain()
                if gemini.is_available():
                    text = gemini.analyze_screen(path, "Read all visible text on this screen exactly as shown.")
                    return ToolResult(success=True, message=text, data={"text": text})
                return ToolResult(success=False, message="Neither pytesseract nor Gemini available for OCR.")
        except Exception as e:
            return ToolResult(success=False, message=f"OCR failed: {str(e)}")
