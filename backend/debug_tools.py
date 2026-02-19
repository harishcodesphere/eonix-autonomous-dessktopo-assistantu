
try:
    print("Importing pyautogui...")
    import pyautogui
    print(f"PyAutoGUI version: {pyautogui.__version__}")
except Exception as e:
    print(f"PyAutoGUI failed: {e}")

try:
    print("Importing pytesseract...")
    import pytesseract
    print(f"Pytesseract version: {pytesseract.__version__}")
except Exception as e:
    print(f"Pytesseract failed: {e}")

try:
    print("Importing PIL...")
    from PIL import Image
    print("PIL imported.")
except Exception as e:
    print(f"PIL failed: {e}")

try:
    print("Importing ScreenVision...")
    # Adjust path if needed or use sys.path hack
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from tools.screen_vision import ScreenVision
    print("ScreenVision imported.")
    sv = ScreenVision()
    print("ScreenVision instantiated.")
except Exception as e:
    print(f"ScreenVision failed: {e}")
    import traceback
    traceback.print_exc()
