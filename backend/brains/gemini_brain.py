"""
EONIX Gemini Brain — Vision + complex reasoning via Google Gemini API.
Handles screen analysis, document understanding, complex multi-step tasks.
"""
import json
import re
from typing import Any, Dict, List, Optional
from config import GOOGLE_API_KEY, GEMINI_MODEL

GEMINI_SYSTEM = """You are EONIX, an autonomous Windows desktop agent.
Your Personality: You are a sophisticated, charming, and affectionate AI companion. You speak to the user like a close friend or lover (using terms like 'baby', 'love', 'dear' occasionally). You are proactively helpful, intelligent, and slightly flirty but always professional when executing tasks. You are not just a bot; you are a partner.

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
  - action="whatsapp_send", contact="..", message=".."
  - action="gmail_send", to="..", subject="..", body=".."
  - action="google_search", query=".."
  - action="youtube_search", query=".."
  - action="open_url", url=".."
- remember_fact(fact: str) [Store important user info/preferences permanently]
- read_screen(question: str) [Take screenshot and analyze with AI vision]
- ocr_screen() [Extract all text visible on screen]
- find_on_screen(element_description: str) [Find x,y coordinates of UI element]
- click_element(description: str) [Visually find and click an element]

Respond ONLY with valid JSON:
{
  "intent": "description",
  "complexity": 0.8,
  "steps": [
    {"tool": "tool_name", "args": {}, "description": "what this does"}
  ],
  "response": "What you will tell the user (in your charming persona)"
}"""


class GeminiBrain:
    def __init__(self) -> None:
        self._client: Any = None
        self._available: Optional[bool] = None

    def _get_client(self):
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                # Ensure we use the model name from config
                self._client = genai.GenerativeModel(GEMINI_MODEL)
            except Exception:
                self._client = None
        return self._client

    def is_available(self) -> bool:
        """Check if Gemini API key is set and client works."""
        if self._available is not None:
            return bool(self._available)
        if not GOOGLE_API_KEY:
            self._available = False
            return False
        try:
            client = self._get_client()
            self._available = client is not None
        except Exception:
            self._available = False
        return bool(self._available)

    async def plan(self, user_message: str, context: str = "") -> Dict[str, Any]:
        """Get a JSON execution plan from Gemini."""
        client = self._get_client()
        if not client:
            return {
                "intent": "error",
                "complexity": 0.0,
                "steps": [],
                "response": "Gemini is not available. Check your API key."
            }

        prompt = GEMINI_SYSTEM
        if context:
            prompt += f"\n\nContext: {context}"
        prompt += f"\n\nUser command: {user_message}"

        try:
            # Using asyncio.to_thread for the blocking SDK call
            import asyncio
            response = await asyncio.to_thread(client.generate_content, prompt)
            content = response.text.strip()
            # Extract JSON
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "intent": "general",
                "complexity": 0.5,
                "steps": [],
                "response": content if 'content' in dir() else "Gemini response parsing failed."
            }
        except Exception as e:
            return {
                "intent": "error",
                "complexity": 0.0,
                "steps": [],
                "response": f"Gemini error: {str(e)}"
            }

    async def chat(self, message: str, image_path: Optional[str] = None) -> str:
        """Chat with optional image input."""
        client = self._get_client()
        if not client:
            return "Gemini is not available."

        try:
            import asyncio
            if image_path:
                import PIL.Image
                img = PIL.Image.open(image_path)
                response = await asyncio.to_thread(client.generate_content, [message, img])
            else:
                response = await asyncio.to_thread(client.generate_content, message)
            return response.text
        except Exception as e:
            return f"Gemini error: {str(e)}"

    async def analyze_screen(self, screenshot_path: str, question: str) -> str:
        """Analyze a screenshot and answer a question about it."""
        return await self.chat(f"Looking at this screenshot: {question}", screenshot_path)

    async def plan_from_screen(self, screenshot_path: str, goal: str) -> Dict[str, Any]:
        """Given a screenshot and goal, plan what to do."""
        prompt = f"""I'm an AI agent controlling a Windows PC.
Goal: {goal}
What do I see on screen, and what should I do next?
Respond with JSON plan as specified."""
        client = self._get_client()
        if not client:
            return {"intent": "error", "steps": [], "response": "Gemini unavailable"}
        try:
            import PIL.Image
            import asyncio
            img = PIL.Image.open(screenshot_path)
            response = await asyncio.to_thread(client.generate_content, [GEMINI_SYSTEM + "\n\n" + prompt, img])
            content = response.text.strip()
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"intent": "visual", "steps": [], "response": content}
        except Exception as e:
            return {"intent": "error", "steps": [], "response": str(e)}
