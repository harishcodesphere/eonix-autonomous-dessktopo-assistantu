"""
Script to verify Screen Vision implementation.
"""
import sys
import os
import time

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from tools import ToolRegistry

def test_vision():
    print("Initializing ToolRegistry...")
    try:
        registry = ToolRegistry()
        print("ToolRegistry initialized.")
    except Exception as e:
        print(f"FAILED to initialize ToolRegistry: {e}")
        return

    print("\n--- Testing Screen Vision Tools ---")
    
    # 1. Test Screenshot (integrated in read_screen usually, but we can call vision directly if needed)
    # But we should test via registry to ensure mapping is correct.
    
    # 2. Test read_screen
    print("\n[Test] read_screen...")
    try:
        # We pass a simple question. 
        # Note: This requires Gemini API Key to be valid.
        result = registry.execute("read_screen", {"question": "What is the window title?"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"read_screen FAILED: {e}")

    # 3. Test OCR
    print("\n[Test] ocr_screen...")
    try:
        result = registry.execute("ocr_screen", {})
        # Result content might be empty if screen is blank/headless, but should succeed.
        print(f"Result: {str(result)[:100]}...") 
    except Exception as e:
        print(f"ocr_screen FAILED: {e}")

    # 4. Test find_on_screen
    print("\n[Test] find_on_screen...")
    try:
        # This uses Gemini to find coordinates.
        result = registry.execute("find_on_screen", {"element": "Start Button"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"find_on_screen FAILED: {e}")

if __name__ == "__main__":
    test_vision()
