"""
EONIX Task Scheduler — Schedule commands to run at specific times.
"""
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Callable, Optional, List, Dict, Any

SCHEDULE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "schedules.json")

class ScheduledTask:
    def __init__(self, name: str, command: str, run_at: datetime, repeat: Optional[str] = None):
        self.name = name
        self.command = command
        self.run_at = run_at
        self.repeat = repeat  # "daily", "hourly", "weekly", None
        self.completed = False
        self.id = f"{name}_{run_at.timestamp()}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "command": self.command,
            "run_at": self.run_at.isoformat(),
            "repeat": self.repeat,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScheduledTask':
        task = cls(
            name=data["name"],
            command=data["command"],
            run_at=datetime.fromisoformat(data["run_at"]),
            repeat=data.get("repeat")
        )
        task.id = data.get("id", task.id)
        task.completed = data.get("completed", False)
        return task


class TaskScheduler:
    """Manage scheduled tasks."""

    def __init__(self):
        self.tasks: List[ScheduledTask] = []
        self.running = False
        self.on_execute: Optional[Callable] = None
        self._load()

    def _load(self):
        """Load scheduled tasks from disk."""
        try:
            if os.path.exists(SCHEDULE_FILE):
                with open(SCHEDULE_FILE, 'r') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        self.tasks = [ScheduledTask.from_dict(t) for t in data]
        except Exception as e:
            print(f"⚠️ Scheduler load error: {e}")
            self.tasks = []

    def _save(self):
        """Persist scheduled tasks to disk."""
        try:
            os.makedirs(os.path.dirname(SCHEDULE_FILE), exist_ok=True)
            with open(SCHEDULE_FILE, 'w') as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=2)
        except Exception as e:
            print(f"❌ Scheduler save error: {e}")

    def add(self, name: str, command: str, run_at: datetime, repeat: Optional[str] = None) -> ScheduledTask:
        """Add a scheduled task."""
        task = ScheduledTask(name, command, run_at, repeat)
        self.tasks.append(task)
        self._save()
        return task

    def remove(self, task_id: str) -> bool:
        """Remove a scheduled task."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < before:
            self._save()
            return True
        return False

    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all scheduled tasks."""
        return [t.to_dict() for t in self.tasks if not t.completed]

    async def start(self):
        """Start the scheduler loop."""
        self.running = True
        print("⏰ Task Scheduler: ONLINE")
        while self.running:
            try:
                now = datetime.now()
                # Create a copy to iterate safely
                for task in list(self.tasks):
                    if task.completed:
                        continue
                        
                    if now >= task.run_at:
                        # Execute the task
                        print(f"⏰ Executing scheduled task: {task.name}")
                        if self.on_execute:
                            try:
                                callback = self.on_execute
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(task.command)
                                else:
                                    callback(task.command)
                            except Exception as e:
                                print(f"❌ Scheduled task execution error: {e}")

                        # Handle repeat
                        if task.repeat == "daily":
                            task.run_at += timedelta(days=1)
                        elif task.repeat == "hourly":
                            task.run_at += timedelta(hours=1)
                        elif task.repeat == "weekly":
                            task.run_at += timedelta(weeks=1)
                        else:
                            task.completed = True

                        self._save()
            except Exception as e:
                print(f"❌ Scheduler loop error: {e}")
                
            await asyncio.sleep(30)  # Check every 30 seconds

    def stop(self):
        self.running = False
        print("⏰ Task Scheduler: OFFLINE")


# Global instance
scheduler = TaskScheduler()
