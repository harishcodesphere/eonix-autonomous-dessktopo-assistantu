"""
Eonix Entity Extractor
Extracts structured entities from natural language commands.
"""
import json
import re
from loguru import logger
from ai.ollama_client import OllamaClient
from ai.prompts import get_prompt


class EntityExtractor:
    def __init__(self, ai_client: OllamaClient = None):
        self.ai = ai_client or OllamaClient()
        self.system_prompt = get_prompt("entity_extractor")

    async def extract(self, user_input: str) -> list[dict]:
        """
        Extract entities from user input.
        Returns list of dicts: [{type, value, original_text}, ...]
        """
        try:
            raw = await self.ai.generate_response(user_input, system_prompt=self.system_prompt)
            parsed = self._parse_json(raw)
            if parsed and "entities" in parsed:
                return parsed["entities"]
            return self._fallback_extract(user_input)
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return self._fallback_extract(user_input)

    def _parse_json(self, text: str) -> dict | None:
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        return None

    def _fallback_extract(self, text: str) -> list[dict]:
        """Regex-based fallback entity extraction."""
        entities = []

        # File paths (Windows & Unix)
        paths = re.findall(r'[A-Za-z]:\\[\w\\\.\-\s]+|~/[\w/\.\-]+|/[\w/\.\-]+', text)
        for p in paths:
            entities.append({"type": "file_path", "value": p.strip(), "original_text": p})

        # Time expressions
        time_patterns = re.findall(
            r'in \d+ (?:minute|hour|second|day)s?|'
            r'at \d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?|'
            r'tomorrow|tonight|every \w+',
            text, re.IGNORECASE
        )
        for t in time_patterns:
            entities.append({"type": "time_expression", "value": t.strip(), "original_text": t})

        # Numbers
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        for n in numbers:
            entities.append({"type": "number", "value": n, "original_text": n})

        return entities
