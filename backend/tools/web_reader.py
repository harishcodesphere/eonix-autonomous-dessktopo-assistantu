"""
EONIX Web Reader Tool — Fetch, clean, and summarize any webpage.
"""
import re
import html
import urllib.request
import urllib.error
from tools.tool_result import ToolResult


class WebReader:
    name = "read_webpage"
    description = "Fetch and extract readable text from any URL"

    def execute(self, url: str = "", **_) -> ToolResult:
        """Fetch a URL and return cleaned text content (first ~3000 chars)."""
        if not url:
            return ToolResult(success=False, message="No URL provided.")
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EONIX/1.0"
            })
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")

            text = self._html_to_text(raw)
            text = text[:3000]

            if len(text) < 50:
                return ToolResult(success=False, message="Page had no readable content.")

            return ToolResult(success=True, message=f"📄 Content from {url}:\n\n{text}")
        except urllib.error.URLError as e:
            return ToolResult(success=False, message=f"Failed to fetch URL (network): {e}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to fetch URL: {e}")

    @staticmethod
    def _html_to_text(raw_html: str) -> str:
        """Strip HTML tags and return plain text."""
        # Remove script/style blocks
        text = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", "", raw_html, flags=re.S | re.I)
        text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
        text = re.sub(r"</(p|div|li|h[1-6]|tr)>", "\n", text, flags=re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(text)
        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(line for line in lines if line)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
