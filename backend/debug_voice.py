
import os
import sys
import time

print("--- EONIX Voice System Diagnostic ---")

# 1. Test Imports
print("\n1. Testing Imports...")
try:
    import speech_recognition as sr
    print("✅ speech_recognition imported")
except ImportError as e:
    print(f"❌ speech_recognition FAILED: {e}")

try:
    from faster_whisper import WhisperModel
    print("✅ faster_whisper imported")
except ImportError as e:
    print(f"❌ faster_whisper FAILED: {e}")

try:
    import pyttsx3
    print("✅ pyttsx3 imported")
except ImportError as e:
    print(f"❌ pyttsx3 FAILED: {e}")

# 2. Test TTS
print("\n2. Testing TTS (pyttsx3)...")
try:
    engine = pyttsx3.init()
    print("   Engine initialized.")
    # engine.say("Voice system test.") # verify it doesn't crash
    # engine.runAndWait() # blocking, skip for now to avoid hanging if issue
    print("✅ TTS initialized OK")
except Exception as e:
    print(f"❌ TTS FAILED: {e}")

# 3. Test Whisper Load
print("\n3. Testing Whisper Model Load (CPU)...")
try:
    start = time.time()
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print(f"✅ Whisper 'tiny' model loaded in {time.time() - start:.2f}s")
except Exception as e:
    print(f"❌ Whisper Load FAILED: {e}")

print("\n--- Diagnostic Complete ---")
