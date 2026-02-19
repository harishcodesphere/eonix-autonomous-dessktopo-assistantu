"""
EONIX Backend — Main FastAPI Entry Point
"""
import os
import sys
import asyncio
from typing import Any, Optional
from contextlib import asynccontextmanager

# 1. Immediate path setup — ensures all internal imports work
BACKEND_ROOT = os.path.dirname(os.path.abspath(__file__))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

# 2. Guarded imports for third-party libraries
try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, JSONResponse
except ImportError:
    print("❌ Critical Error: FastAPI and dependencies not found. Please install requirements.")
    sys.exit(1)

# 3. Local module imports (guarded)
try:
    from memory.db import init_db
    from api.routes_chat import router as chat_router
    from api.routes_system import router as system_router
    from api.routes_tasks import router as tasks_router
    from api.routes_voice import router as voice_router
    from api.routes_memory import router as memory_router
    from api.routes_ws import router as ws_router, manager as ws_manager, push_alert
    from brains.ollama_brain import OllamaBrain
    from brains.gemini_brain import GeminiBrain
    from brains.claude_brain import ClaudeBrain
    from agent.monitor import system_monitor
    from agent.scheduler import scheduler
    from agent.plugin_loader import plugin_loader
    from tools.voice import voice_system
    from agent.orchestrator import orchestrator as global_orchestrator
except ImportError as e:
    print(f"⚠ Warning: Some local modules failed to load: {e}")
    # We continue as some modules might be optional

# Global orchestrator reference
orchestrator: Any = None 

FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_ROOT), "frontend")
DATA_DIR = os.path.join(BACKEND_ROOT, "data")


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

    # Initialize directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "audio"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "screenshots"), exist_ok=True)
    
    try:
        init_db()
        print("✓ Database initialized")
    except Exception as e:
        print(f"❌ Database Error: {e}")

    # Initialize AI brains
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
    from agent.orchestrator import orchestrator as _orchestrator
    orchestrator = _orchestrator
    
    # Start Voice System
    async def broadcast_voice_status(status):
        if 'ws_manager' in globals():
            await ws_manager.broadcast({"type": "voice_status", "status": status})

    if 'voice_system' in globals():
        voice_system.set_callback(orchestrator.handle_voice_command)
        voice_system.set_status_callback(broadcast_voice_status)
        voice_system.start()
        print("✓ Voice System — READY (Listening)")

    # Start proactive monitor
    if 'system_monitor' in globals():
        system_monitor.on_alert(push_alert)
        asyncio.create_task(system_monitor.start())
        print("✓ Proactive Monitor — ONLINE")

    # Start scheduler
    if 'scheduler' in globals():
        asyncio.create_task(scheduler.start())

    # Load plugins
    if 'plugin_loader' in globals():
        plugin_results = plugin_loader.load_all()
        loaded_count = sum(1 for r in plugin_results.values() if r["success"])
        print(f"✓ Plugins: {loaded_count}/{len(plugin_results)} loaded")

    print(f"\n🚀 EONIX running at: http://127.0.0.1:8000")
    print("="*50 + "\n")

    yield

    # ── Shutdown ─────────────────────────────────────────────
    print("\n🛑 EONIX shutting down...")
    
    if 'voice_system' in globals():
        voice_system.stop()
    if 'system_monitor' in globals():
        system_monitor.stop()
    if 'scheduler' in globals():
        scheduler.stop()


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

# ── API Routes (Include only if loaded) ──────────────────────
try:
    app.include_router(chat_router, prefix="/api", tags=["chat"])
    app.include_router(system_router, prefix="/api", tags=["system"])
    app.include_router(tasks_router, prefix="/api", tags=["tasks"])
    app.include_router(voice_router, prefix="/api", tags=["voice"])
    app.include_router(memory_router, prefix="/api", tags=["memory"])
    app.include_router(ws_router, tags=["websocket"])
except NameError:
    pass

# ── Briefing Endpoint ────────────────────────────────────────
@app.get("/api/briefing")
async def get_briefing():
    """Get a daily briefing summary."""
    try:
        from agent.briefing import daily_briefing
        briefing = await daily_briefing.generate()
        text = daily_briefing.format_text(briefing)
        return {"briefing": briefing, "text": text}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ── Static Files ─────────────────────────────────────────────
if os.path.exists(DATA_DIR):
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
    try:
        import uvicorn
        uvicorn.run(
            "main:app", 
            host="127.0.0.1", 
            port=8000, 
            reload=True,
            log_level="warning"
        )
    except ImportError:
        print("❌ Uvicorn not found. Please install it.")
