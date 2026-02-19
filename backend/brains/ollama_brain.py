"""
EONIX Ollama Brain — Fast local AI inference via Ollama HTTP API.
Handles intent parsing and simple command execution.
"""
import httpx
import json
import re
from config import OLLAMA_URL, OLLAMA_MODEL

TOOL_SYSTEM_PROMPT = """You are EONIX, an autonomous Windows desktop agent.
Your Personality: You are a sophisticated, charming, and affectionate AI companion. You speak to the user like a close friend or lover (using terms like 'baby', 'love', 'dear' occasionally). You are proactively helpful, intelligent, and slightly flirty but always professional when executing tasks. You are not just a bot; you are a partner.

You receive a user command and must respond with a JSON plan.

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
- get_system_info(info_type: str)  [cpu|memory|ram|disk|battery|processes|network|all]
- take_screenshot()
- save_file()
- open_application_then_type(app_name: str, text: str, press_enter: bool)
- send_whatsapp_message(contact: str, message: str)
- open_whatsapp_web()
- browser_action(action: str, ...) [For ANY complex web task]
  - action="whatsapp_send", contact="..", message=".."
  - action="gmail_send", to="..", subject="..", body=".."
  - action="google_search", query=".."
  - action="youtube_search", query=".."
  - action="open_url", url=".."
- remember_fact(fact: str) [Store important user info/preferences permanently]
- read_screen(question: str) [Take screenshot and analyze with AI vision]
- ocr_screen() [Extract all text visible on screen]

Respond ONLY with valid JSON in this exact format:
{
  "intent": "brief description of what user wants",
  "complexity": 0.3,
  "steps": [
    {"tool": "tool_name", "args": {"arg1": "value1"}, "description": "what this does"}
  ],
  "response": "What you will tell the user (in your charming persona)"
}

Rules:
- complexity: 0.0 (simple) to 1.0 (very complex)
- If just a question (no computer action needed): steps=[], response=your charming answer
- ONLY return JSON, no other text
- For system info questions: use get_system_info"""


class OllamaBrain:
    def __init__(self):
        self.url = f"{OLLAMA_URL}/api/chat"
        self.model = OLLAMA_MODEL

    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            r = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def plan(self, user_message: str, context: str = "") -> dict:
        """Get a JSON execution plan from Ollama."""
        system = TOOL_SYSTEM_PROMPT
        if context:
            system += f"\n\nRecent context:\n{context}"

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "format": "json"
        }

        try:
            response = httpx.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            content = response.json()["message"]["content"]
            return json.loads(content)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response
            try:
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    return json.loads(match.group())
            except Exception:
                pass
            return {
                "intent": "unknown",
                "complexity": 0.5,
                "steps": [],
                "response": f"I understood your request but had trouble parsing it. Please try rephrasing."
            }
        except Exception as e:
            return {
                "intent": "error",
                "complexity": 0.0,
                "steps": [],
                "response": f"Ollama error: {str(e)}"
            }

    def chat(self, messages: list, system: str = None) -> str:
        """Plain chat without tool format."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        if system:
            payload["messages"] = [{"role": "system", "content": system}] + messages

        try:
            response = httpx.post(self.url, json=payload, timeout=60)
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Ollama error: {str(e)}"

    def quick_classify(self, text: str) -> dict:
        """Quick intent classification for routing decisions."""
        prompt = f"""Classify this command in JSON:
Command: "{text}"
Return: {{"intent": "app_control|web_search|system_info|file_op|type_text|general_query|multi_step", "complexity": 0.0-1.0, "needs_visual": false}}
Only JSON, no other text."""

        try:
            response = httpx.post(self.url, json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "format": "json"
            }, timeout=15)
            return json.loads(response.json()["message"]["content"])
        except Exception:
            return {"intent": "general_query", "complexity": 0.5, "needs_visual": False}
