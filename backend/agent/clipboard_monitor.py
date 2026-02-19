import time
import threading
import pyperclip
import re
import logging
import asyncio
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ClipboardMonitor(threading.Thread):
    def __init__(self, push_alert_callback, loop):
        super().__init__()
        self.daemon = True
        self.paused = False
        self.last_content = ""
        self.push_alert = push_alert_callback # Async callback
        self.loop = loop # Main event loop
        self.running = True

    def run(self):
        logger.info("Clipboard Monitor started.")
        # Initialize with current content to avoid triggering on startup
        try:
            self.last_content = pyperclip.paste()
        except Exception:
            self.last_content = ""

        while self.running:
            if not self.paused:
                try:
                    current_content = pyperclip.paste()
                    if current_content != self.last_content:
                        self.last_content = current_content
                        if current_content.strip():
                            self._analyze_and_suggest(current_content)
                except Exception as e:
                    logger.error(f"Clipboard Error: {e}")
            
            time.sleep(2.0)

    def pause(self):
        self.paused = True
        logger.info("Clipboard Monitor paused.")

    def resume(self):
        self.paused = False
        # Reset last content to avoid re-triggering old stuff
        try:
            self.last_content = pyperclip.paste()
        except: pass
        logger.info("Clipboard Monitor resumed.")

    def stop(self):
        self.running = False

    def _analyze_and_suggest(self, text: str):
        suggestions = []
        text = text.strip()
        
        # 1. URL Detection
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        if re.match(url_pattern, text):
            suggestions = [
                {"label": "Summarize Page", "action": "summarize_url", "text": text},
                {"label": "Open in Browser", "action": "open_url", "text": text},
                {"label": "Archive", "action": "archive_url", "text": text}
            ]
        
        # 2. Email Detection
        elif re.match(r"[^@]+@[^@]+\.[^@]+", text):
            suggestions = [
                {"label": "Compose Email", "action": "compose_email", "text": text},
                {"label": "Search Contacts", "action": "search_contacts", "text": text}
            ]

        # 3. Code Detection (heuristic)
        elif self._is_code(text):
            suggestions = [
                {"label": "Explain Code", "action": "chat", "text": f"Explain this code:\n```\n{text[:1000]}\n```"},
                {"label": "Find Bugs", "action": "chat", "text": f"Find bugs in this code:\n```\n{text[:1000]}\n```"},
                {"label": "Refactor", "action": "chat", "text": f"Refactor this code:\n```\n{text[:1000]}\n```"}
            ]

        # 4. Text (Default)
        else:
            if len(text) > 20:
                suggestions = [
                    {"label": "Summarize", "action": "chat", "text": f"Summarize this:\n{text}"},
                    {"label": "Translate", "action": "chat", "text": f"Translate to English:\n{text}"},
                    {"label": "Improve Writing", "action": "chat", "text": f"Improve this writing:\n{text}"}
                ]

        if suggestions and self.push_alert and self.loop:
            asyncio.run_coroutine_threadsafe(self.push_alert({
                "type": "suggestion",
                "suggestions": suggestions
            }), self.loop)

    def _is_code(self, text: str) -> bool:
        indicators = ["def ", "import ", "class ", "{", "}", "function", "var ", "const ", "=>", ";", "#include", "public ", "private "]
        count = sum(1 for i in indicators if i in text)
        return count >= 2 or ("\n" in text and "    " in text and ("=" in text or "(" in text))
