import sys
import os

backend_dir = os.getcwd()
sys.path.append(backend_dir)

print(f"Current Path: {sys.path}")

try:
    from brains.ollama_brain import OllamaBrain
    print("OllamaBrain OK")
    from brains.gemini_brain import GeminiBrain
    print("GeminiBrain OK")
    from tools import ToolRegistry
    print("ToolRegistry OK")
    from agent.router import route, parse_brain_prefix
    print("Router OK")
    from memory.db import get_db, init_db
    print("DB OK")
    from agent.personality import PersonalityEngine
    print("PersonalityEngine OK")
    from ai.chatbot import chatbot as chatbot_engine
    print("ChatbotEngine OK")
    
    print("\nALL IMPORTS SUCCESSFUL")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"\nIMPORT FAILED: {e}")
