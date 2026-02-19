from fastapi import APIRouter
from pydantic import BaseModel
import logging

# We need a reference to the global clipboard monitor instance
# Ideally this would be dependency injected, but for now we'll access it via a global registered in main
# OR we can export a router and have main attach the instance later.
# Let's use a simple global reference pattern or just import if it was a singleton.
# Since it's created in main, we'll need a way to access it.

from typing import Optional

router = APIRouter()
clipboard_monitor_instance = None # To be set by main.py

class ActionResponse(BaseModel):
    status: str
    message: str

@router.post("/pause", response_model=ActionResponse)
async def pause_clipboard():
    if clipboard_monitor_instance:
        clipboard_monitor_instance.pause()
        return {"status": "success", "message": "Clipboard monitor paused"}
    return {"status": "error", "message": "Clipboard monitor not initialized"}

@router.post("/resume", response_model=ActionResponse)
async def resume_clipboard():
    if clipboard_monitor_instance:
        clipboard_monitor_instance.resume()
        return {"status": "success", "message": "Clipboard monitor resumed"}
    return {"status": "error", "message": "Clipboard monitor not initialized"}

def set_monitor_instance(instance):
    global clipboard_monitor_instance
    clipboard_monitor_instance = instance
