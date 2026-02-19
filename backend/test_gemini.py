
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

try:
    response = model.generate_content("Hello, are you working?")
    print("Response from Gemini:")
    print(response.text)
    print("\nGEMINI IS WORKING!")
except Exception as e:
    print(f"GEMINI FAILED: {e}")
