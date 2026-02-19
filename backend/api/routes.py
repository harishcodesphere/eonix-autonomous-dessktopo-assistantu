"""
Eonix API Routes
REST API endpoints for the frontend and external integrations.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from core.orchestrator import orchestrator
from api.dependencies import verify_api_key
from plugins.manager import PluginManager

router = APIRouter(dependencies=[Depends(verify_api_key)])
plugin_manager = PluginManager()


# --- Models ---
class CommandRequest(BaseModel):
    command: str
    context: Optional[Dict[str, Any]] = None

class ActionRequest(BaseModel):
    action: str
    params: Optional[Dict[str, Any]] = {}

class VoiceRequest(BaseModel):
    text: str


# --- Core Endpoints ---
@router.post("/command")
async def execute_command(request: CommandRequest):
    """Execute a natural language command via the Orchestrator."""
    result = await orchestrator.process_command(request.command)
    return result

@router.get("/health")
async def health_check():
    """Check backend health status."""
    return {"status": "healthy", "version": "1.0.0"}


# --- System Endpoints ---
@router.get("/system/stats")
async def get_system_stats():
    """Get real-time system statistics."""
    return await orchestrator.system_monitor.get_stats()

@router.get("/system/processes")
async def list_processes():
    """List running processes."""
    return orchestrator.process_manager.get_processes()

@router.post("/system/process/kill")
async def kill_process(pid: int):
    """Terminate a process by PID."""
    success = orchestrator.process_manager.kill_process(pid)
    if success:
        return {"status": "success", "message": f"Process {pid} terminated"}
    raise HTTPException(status_code=400, detail=f"Failed to kill process {pid}")


# --- File System Endpoints ---
@router.get("/files/list")
async def list_files(path: str = "."):
    """List files in a directory."""
    return orchestrator.file_manager.list_files(path)


# --- Plugin Endpoints ---
@router.get("/plugins")
async def list_plugins():
    """List all available plugins."""
    # Ensure plugins are loaded
    if not plugin_manager.plugins:
        await plugin_manager.load_all()
    return plugin_manager.list_plugins()

@router.post("/plugins/{plugin_name}/execute")
async def execute_plugin_action(plugin_name: str, request: ActionRequest):
    """Execute a specific action on a plugin."""
    result = await plugin_manager.execute_plugin(plugin_name, request.action, request.params)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result


# --- Voice Endpoints ---
@router.post("/voice/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe uploaded audio file (STT)."""
    # In a real app, save file to temp and pass to Whisper
    # orchestrator.voice_processor.transcribe(...)
    return {"status": "success", "text": "Transcription not yet implemented in API"}

@router.post("/voice/synthesize")
async def synthesize_speech(request: VoiceRequest):
    """Convert text to speech (TTS)."""
    # orchestrator.voice_processor.synthesize(...)
    return {"status": "success", "audio_url": "/static/audio/output.wav"}
