"""
EONIX Voice Engine — Text-to-Speech (TTS)
Uses pyttsx3 for offline, low-latency speech synthesis.
"""
import pyttsx3
import asyncio
import functools
from typing import Optional

# Global instance to prevent multiple engine initializations
_engine: Optional[pyttsx3.Engine] = None

def _get_engine() -> Optional[pyttsx3.Engine]:
    global _engine
    if _engine is None:
        try:
            _engine = pyttsx3.init()
            # Configure voice
            voices = _engine.getProperty('voices')
            # Try to find a good female voice (Zira on Windows)
            if voices:
                for v in voices:
                    if "Zira" in v.name or "zira" in v.name:
                        _engine.setProperty('voice', v.id)
                        break
            _engine.setProperty('rate', 170)  # Slightly faster than default
            _engine.setProperty('volume', 1.0)
        except Exception as e:
            print(f"TTS Init Error: {e}")
            _engine = None
    return _engine

class VoiceEngine:
    def __init__(self) -> None:
        self.is_speaking: bool = False
        self.voice: str = "en-GB-SoniaNeural"

    async def speak(self, text: str) -> None:
        """
        Speak text using pyttsx3.
        Must run in a separate thread because pyttsx3 runAndWait is blocking.
        """
        if not text:
            return

        self.is_speaking = True
        print(f"🗣️ EONIX: {text}")
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._speak_sync, text)
        
        self.is_speaking = False

    def _speak_sync(self, text: str) -> None:
        """Blocking synchronous speech function."""
        try:
            engine = _get_engine()
            if engine:
                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    def stop(self) -> None:
        """Stop currently playing speech."""
        try:
            engine = _get_engine()
            if engine:
                engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"TTS Stop Error: {e}")

# Global instance
voice_engine = VoiceEngine()
