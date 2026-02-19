"""
Eonix Response Generator
Generates natural language responses from execution results.
"""
from loguru import logger
from ai.ollama_client import OllamaClient
from ai.prompts import get_prompt


class ResponseGenerator:
    def __init__(self, ai_client: OllamaClient = None):
        self.ai = ai_client or OllamaClient()
        self.system_prompt = get_prompt("response_generator")

    async def generate(self, command: str, intent: dict, results: list[dict]) -> str:
        """
        Generate a natural language response summarizing execution results.
        """
        try:
            prompt = f"""User's original command: "{command}"
Intent: {intent.get('intent', 'unknown')}

Execution results:
"""
            for r in results:
                status = r.get("status", "unknown")
                action = r.get("action", "unknown")
                result_data = r.get("result", r.get("error", "no data"))
                prompt += f"- [{status}] {action}: {result_data}\n"

            prompt += "\nGenerate a concise, friendly response summarizing what happened."

            response = await self.ai.generate_response(prompt, system_prompt=self.system_prompt)
            return response.strip()

        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            # Fallback: construct a simple response
            return self._fallback_response(results)

    def _fallback_response(self, results: list[dict]) -> str:
        """Build a response without AI when LLM is unavailable."""
        successes = [r for r in results if r.get("status") == "success"]
        failures = [r for r in results if r.get("status") != "success"]

        parts = []
        if successes:
            parts.append(f"✅ {len(successes)} task(s) completed successfully.")
        if failures:
            parts.append(f"❌ {len(failures)} task(s) failed.")
            for f in failures:
                parts.append(f"  - {f.get('action', 'unknown')}: {f.get('error', 'unknown error')}")

        return " ".join(parts) if parts else "Done."
