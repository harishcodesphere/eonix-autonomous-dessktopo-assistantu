"""
Eonix Intent Classifier
Uses Ollama/Mistral to classify user commands into actionable intents.
"""
import json
from loguru import logger
from ai.ollama_client import OllamaClient
from ai.prompts import get_prompt


class IntentClassifier:
    def __init__(self, ai_client: OllamaClient = None):
        self.ai = ai_client or OllamaClient()
        self.system_prompt = get_prompt("intent_classifier")

    async def classify(self, user_input: str) -> dict:
        """
        Classify user input into an intent category.
        Returns dict with: intent, action, entities, confidence
        """
        try:
            raw_response = await self.ai.generate_response(
                prompt=user_input,
                system_prompt=self.system_prompt,
            )

            # Extract JSON from response
            result = self._parse_json(raw_response)
            if result:
                logger.info(f"Intent classified: {result.get('intent')} (confidence: {result.get('confidence', 0)})")
                return result

            # Fallback: keyword-based classification
            return self._fallback_classify(user_input)

        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return self._fallback_classify(user_input)

    def _parse_json(self, text: str) -> dict | None:
        """Try to extract JSON from AI response."""
        try:
            # Try direct parse
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass

        # Try to find JSON block in text
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

        return None

    def _fallback_classify(self, user_input: str) -> dict:
        """Keyword-based fallback when LLM fails."""
        text = user_input.lower().strip()
        entities = {}

        # 1. Handle Macros (multi-step commands)
        if " and " in text:
            parts = text.split(" and ")
            actions = []
            for part in parts:
                sub_result = self._fallback_classify(part.strip())
                actions.append(sub_result)
            return {
                "intent": "macro",
                "actions": actions,
                "confidence": 0.7
            }

        keyword_map = {
            "app_control": ["open", "close", "launch", "start", "quit"],
            "file_operation": ["file", "folder", "delete", "move", "copy", "rename", "find", "search"],
            "system_info": ["cpu", "ram", "memory", "disk", "process", "battery", "stats"],
            "automation": ["schedule", "remind", "timer", "type", "write", "press", "enter"],
            "settings": ["setting", "config", "theme"],
        }

        # Check for specific intents
        for intent, keywords in keyword_map.items():
            for kw in keywords:
                if kw in text:
                    # Simple entity extraction for common patterns
                    if intent == "app_control":
                        # "open notepad", "launch calculator" -> app_name="notepad"
                        # Remove the keyword and whitespace
                        app_name = text.replace(kw, "", 1).strip()
                        if app_name:
                            entities["app_name"] = app_name
                    
                    elif intent == "file_operation":
                        # "find report.txt" -> path="report.txt"
                        target = text.replace(kw, "", 1).strip()
                        if target:
                            entities["path"] = target

                    elif intent == "automation":
                        # "type hello world" -> text="hello world"
                        if kw in ["type", "write"]:
                            content = text.replace(kw, "", 1).strip()
                            
                            # Simple variable resolution
                            if "my name" in content:
                                content = content.replace("my name", "Harish")
                            
                            entities["text"] = content
                            return {
                                "intent": intent,
                                "action": "type",
                                "entities": entities,
                                "confidence": 0.6
                            }
                        elif kw in ["press", "enter"]:
                            # "press enter" -> key="enter"
                            key = text.replace(kw, "", 1).strip() or kw
                            entities["key"] = key
                            return {
                                "intent": intent,
                                "action": "press",
                                "entities": entities,
                                "confidence": 0.6
                            }

                    return {
                        "intent": intent,
                        "action": kw, # Use the keyword as a proxy for action
                        "entities": entities,
                        "confidence": 0.6
                    }

        return {
            "intent": "general_query",
            "action": "respond",
            "entities": {},
            "confidence": 0.5,
        }
