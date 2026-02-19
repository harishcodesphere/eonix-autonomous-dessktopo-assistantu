"""
EONIX API Package
"""
from .routes_chat import router as chat_router
from .routes_system import router as system_router
from .routes_tasks import router as tasks_router
from .routes_voice import router as voice_router

__all__ = ["chat_router", "system_router", "tasks_router", "voice_router"]
