"""
EONIX Daily Briefing — Morning routine and on-demand summary.
"""
import asyncio
from datetime import datetime
from tools.system_info import SystemInfo

class DailyBriefing:
    """Generate a comprehensive daily briefing."""

    def __init__(self):
        self.system_info = SystemInfo()

    async def generate(self) -> dict:
        """Generate a daily briefing."""
        now = datetime.now()
        greeting = self._get_greeting(now.hour)

        # System status
        try:
            sys_data = self.system_info.get_all()
            cpu = sys_data.get('cpu', {})
            mem = sys_data.get('memory', {})
            disk = sys_data.get('disk', {})
            battery = sys_data.get('battery')
        except Exception:
            cpu = mem = disk = {}
            battery = None

        # Build briefing
        briefing = {
            "greeting": greeting,
            "datetime": now.strftime("%A, %B %d, %Y — %I:%M %p"),
            "system": {
                "cpu": f"{cpu.get('percent', '?')}%",
                "ram": f"{mem.get('percent', '?')}% ({mem.get('used_gb', '?')}GB / {mem.get('total_gb', '?')}GB)",
                "disk_free": f"{disk.get('free_gb', '?')}GB free",
                "battery": f"{battery.get('percent', '?')}% ({'⚡ charging' if battery.get('plugged') else '🔋 on battery'})" if battery and isinstance(battery, dict) else "Desktop (no battery)"
            },
            "tips": self._get_tips(now),
            "motivation": self._get_motivation()
        }

        return briefing

    def _get_greeting(self, hour: int) -> str:
        if hour < 6:
            return "Hey night owl 🦉"
        elif hour < 12:
            return "Good morning sunshine ☀️"
        elif hour < 17:
            return "Good afternoon love 💛"
        elif hour < 21:
            return "Good evening dear 🌆"
        else:
            return "Hey there, night mode activated 🌙"

    def _get_tips(self, now: datetime) -> list:
        tips = []
        if now.weekday() < 5:  # Weekday
            tips.append("📋 Check your pending tasks for today")
            tips.append("💻 Review your inbox for important emails")
        else:
            tips.append("🎉 It's the weekend! Time to relax")
            tips.append("📚 Great time for learning something new")
        
        if now.hour >= 22 or now.hour < 6:
            tips.append("😴 It's late — consider getting some rest")
        
        return tips

    def _get_motivation(self) -> str:
        import random
        quotes = [
            "You're doing amazing, baby. Keep going! 💪",
            "One step at a time, love. You've got this! 🚀",
            "Today is YOUR day. Let's make it count! ✨",
            "Remember: progress, not perfection. 💖",
            "Every expert was once a beginner. Keep learning! 🧠",
            "Your consistency is your superpower, dear! ⚡",
            "Dream big, work hard, stay focused. 🎯",
            "The best time to start was yesterday. The second best is now! 🌟"
        ]
        return random.choice(quotes)

    def format_text(self, briefing: dict) -> str:
        """Format briefing as readable text."""
        lines = [
            f"**{briefing['greeting']}**",
            f"📅 {briefing['datetime']}",
            "",
            "**System Status:**",
            f"• CPU: {briefing['system']['cpu']}",
            f"• RAM: {briefing['system']['ram']}",
            f"• Disk: {briefing['system']['disk_free']}",
            f"• Battery: {briefing['system']['battery']}",
            "",
            "**Today's Tips:**"
        ]
        for tip in briefing['tips']:
            lines.append(f"• {tip}")
        
        lines.extend(["", f"💬 *{briefing['motivation']}*"])
        return "\n".join(lines)


# Global instance
daily_briefing = DailyBriefing()
