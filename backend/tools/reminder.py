"""
EONIX Reminder & Alarm — In-memory timer with WebSocket alert.
"""
import asyncio
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable, Coroutine
from tools.tool_result import ToolResult


class ReminderTool:
    name = "set_reminder"
    description = "Set reminders and alarms that fire as WebSocket alerts"

    def __init__(self):
        self.reminders: List[Dict[str, Any]] = []
        self._next_id = 1
        self._push_alert: Optional[Callable] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def set_alert_callback(self, callback: Callable, loop: asyncio.AbstractEventLoop):
        """Set the push_alert callback and event loop for firing reminders."""
        self._push_alert = callback
        self._loop = loop

    def set_reminder(self, text: str, minutes: float = 0, time_str: str = "", **_) -> ToolResult:
        """Set a reminder. Provide minutes OR time_str (HH:MM)."""
        now = datetime.now()

        if time_str:
            # Parse HH:MM
            try:
                h, m = map(int, time_str.split(":"))
                fire_at = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if fire_at <= now:
                    fire_at += timedelta(days=1)
                delay_sec = (fire_at - now).total_seconds()
            except ValueError:
                return ToolResult(success=False, message=f"Invalid time format: {time_str}. Use HH:MM")
        elif minutes > 0:
            delay_sec = minutes * 60
            fire_at = now + timedelta(seconds=delay_sec)
        else:
            return ToolResult(success=False, message="Provide 'minutes' or 'time_str' (HH:MM)")

        reminder_id = self._next_id
        self._next_id += 1

        reminder = {
            "id": reminder_id,
            "text": text,
            "fire_at": fire_at.strftime("%H:%M:%S"),
            "created": now.strftime("%H:%M:%S"),
            "fired": False,
        }
        self.reminders.append(reminder)

        # Schedule the async fire
        if self._loop and self._push_alert:
            asyncio.run_coroutine_threadsafe(
                self._schedule_fire(reminder_id, text, delay_sec), self._loop
            )

        time_desc = f"at {fire_at.strftime('%H:%M')}" if time_str else f"in {int(minutes)} minute(s)"
        return ToolResult(
            success=True,
            message=f"⏰ Reminder set: \"{text}\" — {time_desc}",
            data=reminder
        )

    async def _schedule_fire(self, reminder_id: int, text: str, delay_sec: float):
        await asyncio.sleep(delay_sec)
        # Mark as fired
        for r in self.reminders:
            if r["id"] == reminder_id:
                r["fired"] = True
                break
        # Push alert
        if self._push_alert:
            await self._push_alert({
                "type": "alert",
                "severity": "info",
                "title": "⏰ Reminder",
                "message": text,
                "suggestion": "Dismiss or snooze"
            })

    def list_reminders(self, **_) -> ToolResult:
        """List all active (unfired) reminders."""
        active = [r for r in self.reminders if not r["fired"]]
        if not active:
            return ToolResult(success=True, message="📋 No active reminders.")
        lines = [f"  {r['id']}. \"{r['text']}\" — fires at {r['fire_at']}" for r in active]
        msg = "📋 Active reminders:\n" + "\n".join(lines)
        return ToolResult(success=True, message=msg, data=active)

    @staticmethod
    def parse_time_from_text(text: str) -> Dict[str, Any]:
        """Extract minutes or time from natural language."""
        result: Dict[str, Any] = {"text": text, "minutes": 0, "time_str": ""}

        # "in 5 minutes" / "in 30 mins" / "in 1 hour"
        m = re.search(r"in\s+(\d+)\s*(min|minute|minutes|mins|hr|hour|hours|sec|seconds|secs)", text, re.I)
        if m:
            val = int(m.group(1))
            unit = m.group(2).lower()
            if "hr" in unit or "hour" in unit:
                result["minutes"] = val * 60
            elif "sec" in unit:
                result["minutes"] = val / 60
            else:
                result["minutes"] = val
            # Remove time part from text
            result["text"] = text[:m.start()].strip()
            if not result["text"]:
                result["text"] = "Reminder"
            return result

        # "at 14:30" / "at 8:00"
        m = re.search(r"at\s+(\d{1,2}:\d{2})", text)
        if m:
            result["time_str"] = m.group(1)
            result["text"] = text[:m.start()].strip()
            if not result["text"]:
                result["text"] = "Alarm"
            return result

        return result
