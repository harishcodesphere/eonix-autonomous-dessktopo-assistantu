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

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 2. Guarded imports for third-party libraries
FastAPI = Request = CORSMiddleware = StaticFiles = FileResponse = JSONResponse = None
try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, JSONResponse
except ImportError:
    print("ERROR: Critical Error: FastAPI and dependencies not found. Please install requirements.")
    sys.exit(1)

# 3. Local module imports (guarded)
init_db = chat_router = system_router = tasks_router = voice_router = memory_router = ws_router = ws_manager = push_alert = None
OllamaBrain = GeminiBrain = ClaudeBrain = system_monitor = scheduler = plugin_loader = voice_system = global_orchestrator = None
briefing_router = workflows_router = briefing = workflow_engine = clipboard_monitor = clipboard_router = None
ClipboardMonitor = None
analytics_router = usage_tracker_instance = None
security_router = security_monitor_bg = None

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
    from api.routes_briefing import router as briefing_router
    from api.routes_workflows import router as workflows_router
    from agent.briefing import briefing
    from agent.workflow_engine import workflow_engine
    from agent.clipboard_monitor import ClipboardMonitor
    from api.routes_clipboard import router as clipboard_router, set_monitor_instance
    from api.routes_analytics import router as analytics_router
    from tools.usage_tracker import usage_tracker as usage_tracker_instance
    import asyncio
except Exception as e:
    print(f"WARNING: Some local modules failed to load: {e}")
    # We continue as some modules might be optional

try:
    from api.routes_security import router as security_router
    from tools.security_monitor import security_monitor_bg
except Exception as e:
    print(f"WARNING: Security module failed to load: {e}")
    import traceback; traceback.print_exc()

# Global orchestrator reference
orchestrator: Any = None 

FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_ROOT), "frontend")
DATA_DIR = os.path.join(BACKEND_ROOT, "data")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────
    print("\n" + "="*50)
    # Keep startup banner ASCII-only to avoid UnicodeEncodeError on Windows consoles.
    print("  EONIX")
    print("  Your Local JARVIS - Autonomous Desktop Agent")
    print("="*50)

    # Initialize directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "audio"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "screenshots"), exist_ok=True)
    
    try:
        init_db()
        print("OK: Database initialized")
    except Exception as e:
        print(f"ERROR: Database Error: {e}")

    # Initialize AI brains
    ollama = OllamaBrain() if OllamaBrain else None
    gemini = GeminiBrain() if GeminiBrain else None
    claude = ClaudeBrain() if ClaudeBrain else None

    if ollama and ollama.is_available():
        print("OK: Ollama (Local AI) — ONLINE")
    else:
        print("WARNING: Ollama — OFFLINE (start with: ollama serve)")

    if gemini and gemini.is_available():
        print("OK: Gemini — ONLINE")
    else:
        print("WARNING: Gemini — API key not set or unavailable")

    if claude and claude.is_available():
        print("OK: Claude — ONLINE")
    else:
        print("WARNING: Claude — API key not set or unavailable")

    # Initialize Orchestrator
    global orchestrator
    from agent.orchestrator import orchestrator as _orchestrator
    orchestrator = _orchestrator
    
    # Start Voice System
    async def broadcast_voice_status(status):
        if ws_manager:
            await ws_manager.broadcast({"type": "voice_status", "status": status})

    if voice_system and orchestrator:
        voice_system.set_callback(orchestrator.handle_voice_command)
        voice_system.set_status_callback(broadcast_voice_status)
        voice_system.start()
        print("OK: Voice System — READY (Listening)")

    # Start proactive monitor
    if system_monitor:
        system_monitor.on_alert(push_alert)
        asyncio.create_task(system_monitor.start())
        print("OK: Proactive Monitor — ONLINE")

    # Start scheduler
    if scheduler:
        # constant check for 8 AM briefing
        has_briefing = any(t.command == "run_briefing" for t in scheduler.tasks)
        if not has_briefing:
            from datetime import datetime, timedelta
            # Default to 8:00 AM tomorrow
            now = datetime.now()
            briefing_time_str = os.getenv("BRIEFING_TIME", "08:00")
            h, m = map(int, briefing_time_str.split(":"))
            
            run_at = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if run_at <= now:
                run_at += timedelta(days=1)
                
            scheduler.add("Daily Briefing", "run_briefing", run_at, "daily")
            print(f"OK: Scheduled Daily Briefing for {run_at}")

        scheduler.on_execute = execute_scheduled_task
        asyncio.create_task(scheduler.start())

    # Load Workflows
    if workflow_engine:
        workflow_engine.load_workflows()
        print("OK: Workflow Engine — LOADED")

    # Load plugins
    if plugin_loader:
        plugin_results = plugin_loader.load_all()
        loaded_count = sum(1 for r in plugin_results.values() if r["success"])
        print(f"OK: Plugins: {loaded_count}/{len(plugin_results)} loaded")

    # Start Clipboard Monitor
    try:
        global clipboard_monitor
        if ClipboardMonitor:
            # Pass the running loop to the monitor so it can schedule async alerts
            loop = asyncio.get_running_loop()
            clipboard_monitor = ClipboardMonitor(push_alert, loop)
            clipboard_monitor.start()
            set_monitor_instance(clipboard_monitor)
            print("OK: Clipboard Intelligence — ONLINE")
    except Exception as e:
        print(f"WARNING: Clipboard Monitor failed to start: {e}")

    # Start Usage Tracker
    if usage_tracker_instance:
        usage_tracker_instance.start()
        print("OK: App Usage Tracker \u2014 ONLINE")

    # Start Security Monitor
    if security_monitor_bg:
        security_monitor_bg.start()
        print("OK: Security Monitor \u2014 ONLINE")

    print("\nEONIX running at: http://127.0.0.1:8000")
    print("="*50 + "\n")

    yield

    # ── Shutdown ─────────────────────────────────────────────
    print("\nEONIX shutting down...")
    
    if voice_system:
        voice_system.stop()
    if system_monitor:
        system_monitor.stop()
    if scheduler:
        scheduler.stop()
    if usage_tracker_instance:
        usage_tracker_instance.stop()
    if security_monitor_bg:
        security_monitor_bg.stop()
    if clipboard_monitor:
        clipboard_monitor.stop()


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
    if chat_router: app.include_router(chat_router, prefix="/api", tags=["chat"])
    if system_router: app.include_router(system_router, prefix="/api", tags=["system"])
    if tasks_router: app.include_router(tasks_router, prefix="/api", tags=["tasks"])
    if voice_router: app.include_router(voice_router, prefix="/api", tags=["voice"])
    if memory_router: app.include_router(memory_router, prefix="/api", tags=["memory"])
    if ws_router: app.include_router(ws_router, tags=["websocket"])
    if briefing_router: app.include_router(briefing_router, prefix="/api", tags=["briefing"])
    if workflows_router: app.include_router(workflows_router, prefix="/api", tags=["workflows"])
    if clipboard_router: app.include_router(clipboard_router, prefix="/api/clipboard", tags=["clipboard"])
    if analytics_router: app.include_router(analytics_router, prefix="/api", tags=["analytics"])
    if security_router: app.include_router(security_router, prefix="/api", tags=["security"])
except Exception as e:
    print(f"WARNING: Failed to include some routers: {e}")

# ── Scheduler Callback ───────────────────────────────────────
async def execute_scheduled_task(command: str):
    """Callback for the scheduler to execute tasks."""
    print(f"⏰ Scheduler Trigger: {command}")
    
    if command == "run_briefing":
        # 1. Generate Briefing
        try:
            from agent.briefing import briefing
            content = await briefing.generate()
            
            # 2. Push to Frontend
            if push_alert:
                await push_alert({
                    "type": "briefing",
                    "data": content
                })
            
            # 3. Speak it
            text = briefing.format_text(content)
            if voice_system:
                # Use voice system's engine if available, or imports
                try:
                    from tools.voice_engine import voice_engine
                    if voice_engine:
                        await voice_engine.speak(text)
                except:
                    pass
        except Exception as e:
            print(f"Briefing execution error: {e}")

# Register callback
if scheduler:
    scheduler.on_execute = execute_scheduled_task

# ── Briefing Endpoint ────────────────────────────────────────
@app.get("/api/briefing")
async def get_briefing():
    """Get a daily briefing summary."""
    try:
        from agent.briefing import briefing
        content = await briefing.generate()
        text = briefing.format_text(content)
        return {"briefing": content, "text": text}
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
        print("ERROR: Uvicorn not found. Please install it.")
