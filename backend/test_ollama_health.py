import asyncio
import httpx
import sys

async def check_ollama():
    url = "http://localhost:11434/api/tags"
    print(f"Checking Ollama at {url}...")
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)
            if response.status_code == 200:
                print("SUCCESS: Ollama is reachable.")
                models = response.json().get("models", [])
                if not models:
                    print("WARNING: No models found. Run 'ollama pull mistral'")
                else:
                    print("Available models:")
                    for m in models:
                        print(f" - {m['name']}")
            else:
                print(f"FAILURE: Ollama returned status {response.status_code}")
    except Exception as e:
        print(f"FAILURE: Could not reach Ollama: {e}")

if __name__ == "__main__":
    asyncio.run(check_ollama())
