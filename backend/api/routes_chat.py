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


@router.post("/chat")
async def chat(request: ChatRequest):
    """Process a chat message and return response (streaming or JSON)."""

    if request.stream:
        async def event_stream():
            async for event in orchestrator.stream_process(request.message, request.history):
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0)

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
        result = await orchestrator.process(request.message, request.history)
        return {
            "reply": result.reply,
            "brain": result.brain,
            "actions": result.actions,
            "duration_ms": result.duration_ms,
            "task_id": result.task_id,
            "success": result.success
        }
