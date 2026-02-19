"""
EONIX System API — Health, status, brain control.
"""
from fastapi import APIRouter
from agent.orchestrator import orchestrator
from brains.ollama_brain import OllamaBrain
from brains.gemini_brain import GeminiBrain
from tools.system_info import SystemInfo

router = APIRouter()
_ollama = OllamaBrain()
_gemini = GeminiBrain()
_sysinfo = SystemInfo()


@router.get("/health")
async def health():
    """Quick health check."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "name": "EONIX"
    }


@router.get("/system/status")
async def system_status():
    """Full system status including AI brain availability."""
    data = _sysinfo.get_all()
    ollama_ok = _ollama.is_available()
    gemini_ok = _gemini.is_available()
    return {
        **data,
        "brains": {
            "ollama": {"available": ollama_ok, "model": "mistral"},
            "gemini": {"available": gemini_ok, "model": "gemini-2.0-flash"}
        },
        "active_brain": orchestrator._default_brain
    }


@router.get("/system/brain")
async def get_brain():
    """Get current default brain."""
    return {"brain": orchestrator._default_brain}


@router.post("/system/brain")
async def set_brain(body: dict):
    """Set default brain."""
    brain = body.get("brain", "auto")
    if brain not in ("local", "gemini", "auto"):
        return {"error": "Invalid brain. Use: local, gemini, auto"}
    orchestrator.set_default_brain(brain)
    return {"brain": brain, "message": f"Switched to {brain} brain"}
