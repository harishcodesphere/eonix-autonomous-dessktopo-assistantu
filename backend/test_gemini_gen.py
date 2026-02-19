import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

async def test_gemini():
    print(f"Testing Gemini API...")
    if not api_key:
        print("FAILURE: GOOGLE_API_KEY not found in .env")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    start = time.time()
    try:
        response = model.generate_content("Hello")
        duration = time.time() - start
        print(f"SUCCESS: Received Gemini response in {duration:.2f}s")
        print(f"Response: {response.text[:100]}...")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
