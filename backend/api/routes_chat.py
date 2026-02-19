"""
EONIX Chat API — POST /api/chat with SSE streaming.
"""
import json
import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

from agent.orchestrator import orchestrator

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = None
    stream: Optional[bool] = True
    brain: Optional[str] = None


@router.post("/chat")
async def chat(request: ChatRequest):
    """Process a chat message and return response (streaming or JSON)."""

    if request.stream:
        async def event_stream():
            try:
                async for event in orchestrator.stream_process(request.message, request.history, brain_override=request.brain):
                    try:
                        payload = json.dumps(event, default=str)
                    except Exception as ser_err:
                        print(f"[SSE] Serialization error: {ser_err}")
                        payload = json.dumps({"type": "error", "message": str(ser_err)})
                    yield f"data: {payload}\n\n"
                    await asyncio.sleep(0)
            except Exception as stream_err:
                print(f"[SSE] Stream error: {stream_err}")
                import traceback; traceback.print_exc()
                yield f"data: {json.dumps({'type': 'error', 'message': str(stream_err)})}\n\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Access-Control-Allow-Origin": "*"
            }
        )
    else:
        # Non-streaming JSON response
        result = await orchestrator.process(request.message, request.history, brain_override=request.brain)
        return {
            "reply": result.reply,
            "brain": result.brain,
            "actions": result.actions,
            "duration_ms": result.duration_ms,
            "task_id": result.task_id,
            "success": result.success
        }
