"""
Eonix Task Scheduler
APScheduler wrapper for timed and cron-based automation triggers.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Callable, Dict
from loguru import logger


class TaskScheduler:
    """Manages scheduled and recurring tasks."""

    def __init__(self):
        self._tasks: Dict[str, dict] = {}
        self._running = False
        self._loop_task = None

    async def start(self):
        """Start the scheduler."""
        self._running = True
        self._loop_task = asyncio.create_task(self._run_loop())
        logger.info("Task scheduler started")

    async def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._loop_task:
            self._loop_task.cancel()
            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass
        logger.info("Task scheduler stopped")

    def schedule_once(self, task_id: str, delay_seconds: float, callback: Callable, description: str = ""):
        """Schedule a one-time task after a delay."""
        run_at = datetime.utcnow() + timedelta(seconds=delay_seconds)
        self._tasks[task_id] = {
            "type": "once",
            "run_at": run_at,
            "callback": callback,
            "description": description,
            "executed": False,
        }
        logger.info(f"Scheduled one-time task '{task_id}' at {run_at}")

    def schedule_recurring(self, task_id: str, interval_seconds: float, callback: Callable, description: str = ""):
        """Schedule a recurring task at a fixed interval."""
        self._tasks[task_id] = {
            "type": "recurring",
            "interval": interval_seconds,
            "next_run": datetime.utcnow() + timedelta(seconds=interval_seconds),
            "callback": callback,
            "description": description,
        }
        logger.info(f"Scheduled recurring task '{task_id}' every {interval_seconds}s")

    def cancel(self, task_id: str) -> bool:
        """Cancel a scheduled task."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            logger.info(f"Cancelled task: {task_id}")
            return True
        return False

    def list_tasks(self) -> list[dict]:
        """List all scheduled tasks."""
        return [
            {
                "id": tid,
                "type": t["type"],
                "description": t["description"],
                "next_run": t.get("run_at", t.get("next_run", "")).isoformat() if isinstance(t.get("run_at", t.get("next_run")), datetime) else "",
            }
            for tid, t in self._tasks.items()
        ]

    async def _run_loop(self):
        """Main scheduler loop — checks and executes due tasks."""
        while self._running:
            try:
                now = datetime.utcnow()
                to_remove = []

                for task_id, task in list(self._tasks.items()):
                    if task["type"] == "once":
                        if not task["executed"] and now >= task["run_at"]:
                            logger.info(f"Executing scheduled task: {task_id}")
                            try:
                                if asyncio.iscoroutinefunction(task["callback"]):
                                    await task["callback"]()
                                else:
                                    task["callback"]()
                            except Exception as e:
                                logger.error(f"Scheduled task {task_id} failed: {e}")
                            task["executed"] = True
                            to_remove.append(task_id)

                    elif task["type"] == "recurring":
                        if now >= task["next_run"]:
                            logger.info(f"Executing recurring task: {task_id}")
                            try:
                                if asyncio.iscoroutinefunction(task["callback"]):
                                    await task["callback"]()
                                else:
                                    task["callback"]()
                            except Exception as e:
                                logger.error(f"Recurring task {task_id} failed: {e}")
                            task["next_run"] = now + timedelta(seconds=task["interval"])

                for tid in to_remove:
                    del self._tasks[tid]

                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(5)
