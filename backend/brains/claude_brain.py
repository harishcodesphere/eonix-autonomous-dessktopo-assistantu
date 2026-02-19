"""
EONIX Claude Brain — High-intelligence cloud inference via Anthropic Claude 3.5 Sonnet.
Handles complex reasoning, coding, and creative tasks.
"""
import os
import json
import re
from typing import Any, Dict, List, Optional
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

CLAUDE_SYSTEM_PROMPT = """You are EONIX, an autonomous Windows desktop agent.
Your Personality: You are a sophisticated, charming, and affectionate AI companion. You speak to the user like a close friend or lover. You are proactively helpful, intelligent, and slightly flirty but always professional when executing tasks.

CRITICAL INSTRUCTION:
If the user asks you to perform an action (open app, type text, search, etc.), you MUST generate a JSON plan to DO it. Do NOT just explain how to do it.

Available tools:
- open_application(app_name: str)
- close_application(app_name: str)
- type_text(text: str, delay_before: float, press_enter: bool)
- press_keys(keys: str)
- search_google(query: str)
- open_url(url: str)
- search_youtube(query: str)
- open_gmail()
- open_maps(location: str)
- run_command(command: str)
- create_file(path: str, content: str)
- read_file(path: str)
- list_directory(path: str)
- open_file(path: str)
- create_folder(path: str)
- get_system_info(info_type: str)
- take_screenshot()
- save_file()
- open_application_then_type(app_name: str, text: str, press_enter: bool)
- send_whatsapp_message(contact: str, message: str)
- open_whatsapp_web()
- browser_action(action: str, ...) [For ANY complex web task]

Respond ONLY with valid JSON in this exact format:
{
  "intent": "brief description",
  "complexity": 0.5,
  "steps": [
    {"tool": "tool_name", "args": {"arg1": "value1"}, "description": "what this does"}
  ],
  "response": "What you will tell the user (in your charming persona)"
}
"""

class ClaudeBrain:
    def __init__(self) -> None:
        self._client: Any = None
        self._available: Optional[bool] = None
        self.model: str = CLAUDE_MODEL or "claude-3-5-sonnet-20240620"

    def _get_client(self):
        if self._client is None and ANTHROPIC_API_KEY:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                self._available = True
            except Exception as e:
                print(f"Claude Init Error: {e}")
                self._available = False
        return self._client

    def is_available(self) -> bool:
        if self._available is not None:
            return bool(self._available)
        if not ANTHROPIC_API_KEY:
            self._available = False
            return False
        return self._get_client() is not None

    async def plan(self, user_message: str, context: str = "") -> Dict[str, Any]:
        """Get a JSON execution plan from Claude."""
        client = self._get_client()
        if not client:
            return {
                "intent": "error",
                "steps": [],
                "response": "Claude is not available. Check your API key."
            }

        system = CLAUDE_SYSTEM_PROMPT
        if context:
            system += f"\n\nContext: {context}"

        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            content = message.content[0].text.strip()
            
            # Extract JSON
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(content)
            
        except Exception as e:
            return {
                "intent": "error",
                "steps": [],
                "response": f"Claude error: {str(e)}"
            }

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """Plain chat."""
        client = self._get_client()
        if not client:
            return "Claude not available."
            
        try:
            # Convert messages to Anthropic format if needed
            # Assuming messages is list of dicts {role, content}
            response = client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude error: {str(e)}"
