"""
Eonix Ollama Client
Communicates with the local Ollama LLM server for AI processing.
"""
import httpx
from loguru import logger
from config import settings


class OllamaClient:
    """Client for the local Ollama LLM service."""

    def __init__(self, host: str = None, model: str = None):
        self.host = host or settings.OLLAMA_HOST
        self.model = model or settings.OLLAMA_MODEL
        self._available = None

    async def generate_response(self, prompt: str, system_prompt: str = None, stream: bool = False) -> str:
        """
        Generate a response from Ollama.
        Supports optional system prompt for task-specific behavior.
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }
            if system_prompt:
                payload["system"] = system_prompt

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.host}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")

        except httpx.ConnectError:
            logger.warning("Ollama not reachable. Is it running?")
            return "❌ AI Offline: Please start Ollama."
        except httpx.TimeoutException:
            logger.warning("Ollama request timed out")
            return "⚠️ AI Timeout: The model took too long to respond."
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return f"❌ Model Verification Failed: Ensure '{self.model}' is installed via 'ollama pull {self.model}'."
            return f"❌ AI Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return f"❌ System Error: {str(e)}"

    async def chat(self, messages: list[dict], system_prompt: str = None) -> str:
        """
        Chat-style interaction using Ollama's /api/chat endpoint.
        messages: [{"role": "user"|"assistant", "content": "..."}]
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
            }
            if system_prompt:
                payload["messages"] = [{"role": "system", "content": system_prompt}] + messages

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.host}/api/chat",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")

        except httpx.ConnectError:
            logger.warning("Ollama not reachable. Is it running?")
            return "❌ AI Offline: Please start Ollama."
        except httpx.TimeoutException:
            logger.warning("Ollama request timed out")
            return "⚠️ AI Timeout: The model took too long to respond."
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return f"❌ Model Verification Failed: Ensure '{self.model}' is installed via 'ollama pull {self.model}'."
            return f"❌ AI Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return f"❌ System Error: {str(e)}"

    async def check_health(self) -> dict:
        """Check Ollama server health and available models."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.host}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m.get("name", "") for m in models]
                    self._available = True
                    return {
                        "status": "online",
                        "models": model_names,
                        "active_model": self.model,
                        "model_available": self.model in model_names or any(self.model.split(":")[0] in m for m in model_names),
                    }
                self._available = False
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except Exception as e:
            self._available = False
            return {"status": "offline", "error": str(e)}

    async def list_models(self) -> list[str]:
        """List available models on the Ollama server."""
        health = await self.check_health()
        return health.get("models", [])

    @property
    def is_available(self) -> bool:
        return self._available is True
