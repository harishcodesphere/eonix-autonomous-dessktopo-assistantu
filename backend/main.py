"""
EONIX Backend — Main FastAPI Entry Point
"""
import os
import sys
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from memory.db import init_db
from api.routes_chat import router as chat_router
from api.routes_system import router as system_router
from api.routes_tasks import router as tasks_router
from api.routes_voice import router as voice_router
from api.routes_memory import router as memory_router
from api.routes_ws import router as ws_router
from brains.ollama_brain import OllamaBrain
from brains.gemini_brain import GeminiBrain
from brains.claude_brain import ClaudeBrain
from agent.monitor import system_monitor
from api.routes_ws import push_alert
from agent.scheduler import scheduler
from agent.plugin_loader import plugin_loader
from tools.voice import voice_system
from agent.orchestrator import AgentOrchestrator

# Initialize global orchestrator for voice callback
# (This avoids circular import issues by importing INSIDE callback or using global)
orchestrator = None 

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    print("\n" + "="*50)
    print("  ███████╗ ██████╗ ███╗  ██╗██╗██╗  ██╗")
    print("  ██╔════╝██╔═══██╗████╗ ██║██║╚██╗██╔╝")
    print("  █████╗  ██║   ██║██╔██╗██║██║ ╚███╔╝ ")
    print("  ██╔══╝  ██║   ██║██║╚████║██║ ██╔██╗ ")
    print("  ███████╗╚██████╔╝██║ ╚███║██║██╔╝╚██╗")
    print("  ╚══════╝ ╚═════╝ ╚═╝  ╚══╝╚═╝╚═╝  ╚═╝")
    print("  Your Local JARVIS — Autonomous Desktop Agent")
    print("="*50)

    # Initialize database
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "audio"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "screenshots"), exist_ok=True)
    init_db()
    print("✓ Database initialized")

    # Check AI brains
    ollama = OllamaBrain()
    gemini = GeminiBrain()
    claude = ClaudeBrain()

    if ollama.is_available():
        print("✓ Ollama (Local AI) — ONLINE")
    else:
        print("⚠ Ollama — OFFLINE (start with: ollama serve)")

    if gemini.is_available():
        print("✓ Gemini — ONLINE")
    else:
        print("⚠ Gemini — API key not set or unavailable")

    if claude.is_available():
        print("✓ Claude — ONLINE")
    else:
        print("⚠ Claude — API key not set or unavailable")

    # Initialize Orchestrator
    global orchestrator
    orchestrator = AgentOrchestrator()
    
    # Start Voice System
    from api.routes_ws import manager

    async def broadcast_voice_status(status):
        await manager.broadcast({"type": "voice_status", "status": status})

    voice_system.set_callback(orchestrator.handle_voice_command)
    voice_system.set_status_callback(broadcast_voice_status)
    voice_system.start()
    print("✓ Voice System — READY (Listening)")

    # Start proactive monitor
    system_monitor.on_alert(push_alert)
    monitor_task = asyncio.create_task(system_monitor.start())
    print("✓ Proactive Monitor — ONLINE")

    # Start scheduler
    scheduler_task = asyncio.create_task(scheduler.start())

    # Load plugins
    plugin_results = plugin_loader.load_all()
    loaded_count = sum(1 for r in plugin_results.values() if r["success"])
    print(f"✓ Plugins: {loaded_count}/{len(plugin_results)} loaded")

    print(f"\n🚀 EONIX running at: http://127.0.0.1:8000")
    print("="*50 + "\n")

    yield

    # Stop background tasks on shutdown
    voice_system.stop()
    system_monitor.stop()
    monitor_task.cancel()
    scheduler.stop()
    scheduler_task.cancel()

    # ── Shutdown ─────────────────────────────────────────────
    print("\n🛑 EONIX shutting down...")


# ── App Setup ────────────────────────────────────────────────
app = FastAPI(
    title="EONIX",
    version="2.0.0",
    description="Local JARVIS — Autonomous Desktop Agent",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__}
    )

# ── API Routes ───────────────────────────────────────────────
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(system_router, prefix="/api", tags=["system"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(voice_router, prefix="/api", tags=["voice"])
app.include_router(memory_router, prefix="/api", tags=["memory"])
app.include_router(ws_router, tags=["websocket"])

# ── Briefing Endpoint ────────────────────────────────────────
@app.get("/api/briefing")
async def get_briefing():
    """Get a daily briefing summary."""
    from agent.briefing import daily_briefing
    briefing = await daily_briefing.generate()
    text = daily_briefing.format_text(briefing)
    return {"briefing": briefing, "text": text}

# ── Static Files ─────────────────────────────────────────────
# Serve data/audio and data/screenshots
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

# ── Frontend ─────────────────────────────────────────────────
@app.get("/")
async def serve_frontend():
    """Serve the main EONIX frontend."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend not found", "path": index_path})


@app.get("/{path:path}")
async def serve_static(path: str):
    """Serve frontend static files."""
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    # Fallback to index.html for SPA routing
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "Not found"}, status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="warning"
    )
