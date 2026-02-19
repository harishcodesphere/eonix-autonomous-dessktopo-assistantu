"""
EONIX Voice API — Speak text via EdgeTTS.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from tools.voice_engine import voice_engine

router = APIRouter()

class SpeakRequest(BaseModel):
    text: str
    voice: str = "en-GB-SoniaNeural"

@router.post("/voice/speak")
async def speak(request: SpeakRequest):
    """Speak text using the high-quality neural voice."""
    if request.voice:
        voice_engine.voice = request.voice
    
    # We run this as a background task essentially, but for now await it
    # so the frontend knows when it's done.
    await voice_engine.speak(request.text)
    return {"status": "success"}

@router.post("/voice/stop")
async def stop_speech():
    """Stop currently playing speech."""
    voice_engine.stop()
    return {"status": "stopped"}
