"""
Eonix WebSocket Manager
Real-time bidirectional communication with the frontend.
"""
import socketio
from loguru import logger
from core.orchestrator import orchestrator

# Initialize Socket.IO server (async mode)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")
    await sio.emit("response", {"data": "Connected to Eonix Backend"}, room=sid)


@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")


@sio.event
async def command(sid, data):
    """Handle incoming command from frontend."""
    logger.info(f"Received command from {sid}: {data}")
    
    cmd_text = data.get("content", "")
    if not cmd_text:
        return

    # Acknowledge receipt
    await sio.emit("status", {"state": "processing", "message": "Thinking..."}, room=sid)

    # Execute via Orchestrator
    try:
        result = await orchestrator.process_command(cmd_text)
        
        # Send response back
        await sio.emit("response", result, room=sid)
        
    except Exception as e:
        logger.error(f"WebSocket command error: {e}")
        await sio.emit("error", {"message": str(e)}, room=sid)


@sio.event
async def voice_data(sid, data):
    """Handle streaming voice data (future implementation)."""
    # Process audio chunk -> STT -> Command
    pass


# Background task to broadcast system stats
async def broadcast_stats():
    """Push system stats to all clients every 2 seconds."""
    import asyncio
    while True:
        try:
            stats = await orchestrator.system_monitor.get_stats()
            await sio.emit("system_stats", stats)
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Stats broadcast error: {e}")
            await asyncio.sleep(5)
