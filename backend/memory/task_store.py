"""
EONIX Task Store — CRUD operations for task history.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from .db import Task, get_db


def create_task(db: Session, user_input: str, brain_used: str = "local") -> Task:
    task = Task(
        user_input=user_input,
        brain_used=brain_used,
        created_at=datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, **kwargs) -> Optional[Task]:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def get_recent_tasks(db: Session, limit: int = 20) -> List[Task]:
    return db.query(Task).order_by(desc(Task.created_at)).limit(limit).all()


def search_tasks(db: Session, query_text: str, limit: int = 10) -> List[Task]:
    pattern = f"%{query_text}%"
    return db.query(Task).filter(
        or_(Task.user_input.like(pattern), Task.result.like(pattern))
    ).order_by(desc(Task.created_at)).limit(limit).all()


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


def get_success_rate(db: Session) -> float:
    total = db.query(Task).filter(Task.success.isnot(None)).count()
    if total == 0:
        return 0.0
    successful = db.query(Task).filter(Task.success == True).count()
    return round((successful / total) * 100, 1)


def get_task_stats(db: Session) -> Dict[str, Any]:
    total = db.query(Task).count()
    success_rate = get_success_rate(db)
    by_brain = {}
    for brain in ["local", "gemini"]:
        count = db.query(Task).filter(Task.brain_used == brain).count()
        by_brain[brain] = count
    return {
        "total": total,
        "success_rate": success_rate,
        "by_brain": by_brain
    }
