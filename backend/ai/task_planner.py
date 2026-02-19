"""
Eonix Task Planner
Breaks complex user commands into atomic, executable steps.
"""
import json
from loguru import logger
from ai.ollama_client import OllamaClient
from ai.prompts import get_prompt


class TaskPlanner:
    def __init__(self, ai_client: OllamaClient = None):
        self.ai = ai_client or OllamaClient()
        self.system_prompt = get_prompt("task_planner")

    async def plan(self, command: str, intent: dict, context: dict = None) -> dict:
        """
        Create an execution plan for a user command.
        Returns a dict with a list of ordered task steps.
        """
        try:
            prompt = f"""User command: "{command}"
Detected intent: {json.dumps(intent)}
Context: {json.dumps(context or {})}

Break this into atomic executable steps."""

            raw = await self.ai.generate_response(prompt, system_prompt=self.system_prompt)
            plan = self._parse_plan(raw)
            if plan:
                logger.info(f"Task plan created with {len(plan.get('tasks', []))} steps")
                return plan

            # Fallback: single-step plan based on intent
            return self._fallback_plan(command, intent)

        except Exception as e:
            logger.error(f"Task planning failed: {e}")
            return self._fallback_plan(command, intent)

    def _parse_plan(self, text: str) -> dict | None:
        """Extract task plan JSON from AI response."""
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

    def _fallback_plan(self, command: str, intent: dict) -> dict:
        """Create a simple single-step plan from intent."""
        action_map = {
            "file_operation": "file_search",
            "app_control": "app_launch",
            "system_info": "system_stats",
            "automation": "notify_user",
            "general_query": "ai_respond",
        }

        action = action_map.get(intent.get("intent", "general_query"), "ai_respond")

        return {
            "tasks": [
                {
                    "id": 1,
                    "action": action,
                    "params": {"command": command, **intent.get("entities", {})},
                    "description": f"Execute: {command}",
                }
            ],
            "estimated_time": "2s",
        }
