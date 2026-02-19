"""
EONIX Voice System (Jarvis Mode).
Handles Wake Word detection and Speech-to-Text using SpeechRecognition.
"""
import threading
import time
import speech_recognition as sr
from tools.voice_engine import voice_engine

class VoiceSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.callback = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def start_listening(self, callback_function):
        """Start the background listening loop."""
        self.callback = callback_function
        self.is_listening = True
        
        # Run in separate thread to not block API
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("🎙️ Voice System: Listening for commands...")

    def _listen_loop(self):
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio (blocking but in thread)
                    # phrase_time_limit=5 prevents getting stuck
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Recognize speech
                try:
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        print(f"👂 Heard: {text}")
                        # Simple wake word check or direct command
                        if self.callback:
                            self.callback(text)
                except sr.UnknownValueError:
                    pass # Silence
                except sr.RequestError as e:
                    print(f"Speech Service Error: {e}")
                    
            except Exception as e:
                # Timeout is normal
                pass
            
            time.sleep(0.1)

    def stop_listening(self):
        self.is_listening = False

# Global instance
voice_system = VoiceSystem()
