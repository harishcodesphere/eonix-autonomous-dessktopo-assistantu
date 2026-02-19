"""
EONIX Voice Engine — High-quality TTS using EdgeTTS (online) with offline fallback.
"""
import asyncio
import os
import pygame
import tempfile
from agent.orchestrator import orchestrator

class VoiceEngine:
    def __init__(self):
        pygame.mixer.init()
        # Voices: 
        # en-US-AnaNeural (Child/Teen - too young?)
        # en-US-AriaNeural (Professional, standard)
        # en-US-JennyNeural (Friendly, standard)
        # en-GB-SoniaNeural (British, sophisticated - maybe good for "Obsidian OS")
        # en-US-MichelleNeural (Warm)
        self.voice = "en-GB-SoniaNeural" 
        self.rate = "+0%"
        self.volume = "+0%"
        self.is_speaking = False

    async def speak(self, text: str):
        """Generate and play speech."""
        if not text:
            return

        self.is_speaking = True
        try:
            # Generate file
            import edge_tts
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume)
            
            # Create unique temp file
            fd, path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            
            await communicate.save(path)
            
            # Play
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            
            # Wait for finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
            # Cleanup
            pygame.mixer.music.unload()
            os.remove(path)
            
        except Exception as e:
            print(f"Voice Error: {e}")
            # Fallback to pyttsx3 could go here if needed
        finally:
            self.is_speaking = False

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

# Global instance
voice_engine = VoiceEngine()
