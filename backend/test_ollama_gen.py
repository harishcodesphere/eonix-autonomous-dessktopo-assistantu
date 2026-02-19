import asyncio
import httpx
import time

async def test_generate():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": "Hello, how are you?",
        "stream": False
    }
    print(f"Sending prompt to Ollama ({payload['model']})...")
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            duration = time.time() - start
            print(f"SUCCESS: Received response in {duration:.2f}s")
            print(f"Response: {data.get('response', '')[:100]}...")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    asyncio.run(test_generate())
