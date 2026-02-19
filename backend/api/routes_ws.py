"""
EONIX WebSocket — Real-time alerts & notifications push.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from typing import List

router = APIRouter()

class ConnectionManager:
    """Manage WebSocket connections for real-time push."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Send message to all connected clients."""
        disconnected = []
        for conn in self.active_connections:
            try:
                await conn.send_json(message)
            except Exception:
                disconnected.append(conn)
        for conn in disconnected:
            self.disconnect(conn)

    async def send_personal(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except Exception:
            self.disconnect(websocket)


manager = ConnectionManager()


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """WebSocket for real-time system alerts and proactive notifications."""
    await manager.connect(websocket)
    try:
        # Send a welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "EONIX real-time alerts connected 🛡️"
        })

        # Keep the connection alive
        while True:
            # Listen for any client messages (ping/pong, etc.)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                # Client can send "ping" to keep alive
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({"type": "heartbeat"})
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


async def push_alert(alert: dict):
    """Push an alert to all connected WebSocket clients."""
    await manager.broadcast({
        "type": "alert",
        **alert
    })
