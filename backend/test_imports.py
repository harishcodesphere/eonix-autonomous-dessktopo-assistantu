
try:
    print("Testing fastapi...")
    import fastapi
    print("FastAPI OK")
except Exception as e:
    print(f"FastAPI FAILED: {e}")

try:
    print("Testing pydantic...")
    import pydantic
    print("Pydantic OK")
except Exception as e:
    print(f"Pydantic FAILED: {e}")

try:
    print("Testing google-generativeai...")
    import google.generativeai
    print("Google GenerativeAI OK")
except Exception as e:
    print(f"Google GenerativeAI FAILED: {e}")

try:
    print("Testing chromadb...")
    import chromadb
    print("ChromaDB OK")
except Exception as e:
    print(f"ChromaDB FAILED: {e}")

try:
    print("Testing agent.orchestrator...")
    import sys
    import os
    sys.path.append(os.getcwd())
    from agent.orchestrator import orchestrator
    print("Orchestrator OK")
except Exception as e:
    print(f"Orchestrator FAILED: {e}")
