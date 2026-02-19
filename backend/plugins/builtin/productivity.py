"""
Eonix Built-in Plugin: Productivity
Timers, reminders, and focus tools.
"""
import asyncio
from datetime import datetime, timedelta
from plugins.base import PluginBase
from loguru import logger


class ProductivityPlugin(PluginBase):
    name = "Productivity"
    description = "Timers, reminders, Pomodoro, and focus mode"
    version = "1.0.0"

    def __init__(self):
        super().__init__()
        self._reminders = []
        self._pomodoro_active = False

    async def initialize(self):
        logger.info("Productivity plugin initialized")

    async def execute(self, action: str, params: dict):
        actions = {
            "set_reminder": self._set_reminder,
            "list_reminders": self._list_reminders,
            "start_pomodoro": self._start_pomodoro,
            "stop_pomodoro": self._stop_pomodoro,
            "set_timer": self._set_timer,
        }
        handler = actions.get(action)
        if handler:
            return await handler(params)
        return {"error": f"Unknown action: {action}"}

    async def _set_reminder(self, params: dict):
        message = params.get("message", "Reminder!")
        delay_minutes = params.get("delay_minutes", 5)
        remind_at = datetime.utcnow() + timedelta(minutes=delay_minutes)
        self._reminders.append({"message": message, "at": remind_at.isoformat()})
        return {"status": "success", "message": f"Reminder set for {delay_minutes} minutes: {message}"}

    async def _list_reminders(self, params: dict):
        return {"reminders": self._reminders}

    async def _start_pomodoro(self, params: dict):
        duration = params.get("duration", 25)
        self._pomodoro_active = True
        return {"status": "success", "message": f"🍅 Pomodoro started ({duration} min). Focus time!"}

    async def _stop_pomodoro(self, params: dict):
        self._pomodoro_active = False
        return {"status": "success", "message": "Pomodoro stopped. Take a break!"}

    async def _set_timer(self, params: dict):
        seconds = params.get("seconds", 60)
        return {"status": "success", "message": f"⏱ Timer set for {seconds} seconds"}

    def get_commands(self):
        return [
            {"name": "set_reminder", "description": "Set a timed reminder"},
            {"name": "list_reminders", "description": "List active reminders"},
            {"name": "start_pomodoro", "description": "Start a Pomodoro focus session"},
            {"name": "stop_pomodoro", "description": "Stop current Pomodoro"},
            {"name": "set_timer", "description": "Set a countdown timer"},
        ]


Plugin = ProductivityPlugin
