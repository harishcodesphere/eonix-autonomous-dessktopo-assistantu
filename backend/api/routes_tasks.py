"""
EONIX Tasks API — Task history and memory endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from memory.db import get_db
from memory.task_store import get_recent_tasks, get_task_by_id, delete_task, get_task_stats
from memory.preference_store import get_preference, set_preference, get_all_preferences

router = APIRouter()


@router.get("/tasks")
async def list_tasks(limit: int = 20):
    """Get recent task history."""
    db = get_db()
    tasks = get_recent_tasks(db, limit=limit)
    db.close()
    return [
        {
            "id": t.id,
            "user_input": t.user_input,
            "brain_used": t.brain_used,
            "intent": t.intent,
            "result": t.result,
            "success": t.success,
            "duration_ms": t.duration_ms,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in tasks
    ]


@router.get("/tasks/stats")
async def task_stats():
    """Get task statistics."""
    db = get_db()
    stats = get_task_stats(db)
    db.close()
    return stats


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """Get a specific task by ID."""
    db = get_db()
    task = get_task_by_id(db, task_id)
    db.close()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task.id,
        "user_input": task.user_input,
        "brain_used": task.brain_used,
        "intent": task.intent,
        "plan": task.plan,
        "actions": task.actions,
        "result": task.result,
        "success": task.success,
        "duration_ms": task.duration_ms,
        "created_at": task.created_at.isoformat() if task.created_at else None
    }


@router.delete("/tasks/{task_id}")
async def remove_task(task_id: int):
    """Delete a task."""
    db = get_db()
    success = delete_task(db, task_id)
    db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted"}


class PreferenceRequest(BaseModel):
    key: str
    value: str


@router.get("/memory/preferences")
async def list_preferences():
    """Get all user preferences."""
    db = get_db()
    prefs = get_all_preferences(db)
    db.close()
    return prefs


@router.post("/memory/preferences")
async def save_preference(req: PreferenceRequest):
    """Set a user preference."""
    db = get_db()
    pref = set_preference(db, req.key, req.value, source="user")
    db.close()
    return {"key": pref.key, "value": pref.value}
