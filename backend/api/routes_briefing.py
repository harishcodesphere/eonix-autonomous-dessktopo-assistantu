"""
Briefing Routes - API endpoints for Daily Briefing.
"""
from fastapi import APIRouter, HTTPException
from agent.briefing import briefing
from api.routes_ws import push_alert
import asyncio

router = APIRouter()

@router.post("/briefing/run")
async def run_briefing():
    """Manually trigger the daily briefing."""
    try:
        # Generate content
        content = await briefing.generate()
        
        # 1. Send to Frontend (for UI Card)
        await push_alert({
            "type": "briefing",
            "data": content
        })
        
        # 2. Speak it (TTS)
        # We use orchestrator's voice engine connection or direct import
        # 2. Speak it (TTS)
        # We use orchestrator's voice engine connection or direct import
        text = briefing.format_text(content)
        try:
            from tools.voice_engine import voice_engine
            await voice_engine.speak(text)
        except Exception as e:
            print(f"TTS Error: {e}")
            
        return {"status": "success", "briefing": content}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
