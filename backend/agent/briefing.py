"""
Daily Briefing Agent - Aggregates weather, tasks, and motivation for the user.
"""
import os
import httpx
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from memory.db import get_db
from memory.task_store import get_recent_tasks
from brains.ollama_brain import OllamaBrain

BRIEFING_TIME = os.getenv("BRIEFING_TIME", "08:00")
WEATHER_CITY = os.getenv("WEATHER_CITY", "Chennai")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

class DailyBriefing:
    def __init__(self):
        self.ollama = OllamaBrain()

    async def generate(self) -> Dict[str, Any]:
        """Generate the full daily briefing content."""
        print("Generating Daily Briefing...")
        
        # 1. Get Date/Time
        now = datetime.now()
        date_str = now.strftime("%A, %d %B %Y")
        time_str = now.strftime("%I:%M %p")
        
        # 2. Get Weather
        weather = await self._get_weather()
        
        # 3. Get Pending Tasks
        tasks = self._get_pending_tasks()
        
        # 4. Generate Motivation/Greeting using AI
        greeting = await self._generate_greeting(date_str, weather, len(tasks))
        
        return {
            "date": date_str,
            "time": time_str,
            "city": WEATHER_CITY,
            "weather": weather,
            "tasks": tasks,
            "greeting": greeting["greeting"],
            "quote": greeting["quote"]
        }

    async def _get_weather(self) -> Dict[str, Any]:
        """Fetch current weather from OpenWeatherMap."""
        if not OPENWEATHER_API_KEY:
            return {"temp": "--", "condition": "Unknown (No API Key)", "icon": "❓"}
            
        url = f"https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    return {
                        "temp": int(data["main"]["temp"]),
                        "condition": data["weather"][0]["description"].title(),
                        "icon": self._get_weather_icon(data["weather"][0]["icon"])
                    }
        except Exception as e:
            print(f"Weather Error: {e}")
            
        return {"temp": "--", "condition": "Unavailable", "icon": "cloud_off"}

    def _get_weather_icon(self, code: str) -> str:
        """Map OpenWeatherMap icon codes to emojis."""
        mapping = {
            "01d": "☀️", "01n": "🌙",
            "02d": "Qloud", "02n": "☁️",
            "03d": "☁️", "03n": "☁️",
            "04d": "☁️", "04n": "☁️",
            "09d": "🌧️", "09n": "🌧️",
            "10d": "🌦️", "10n": "🌧️",
            "11d": "⚡", "11n": "⚡",
            "13d": "❄️", "13n": "❄️",
            "50d": "🌫️", "50n": "🌫️"
        }
        return mapping.get(code, "🌤️")

    def _get_pending_tasks(self) -> List[str]:
        """Get top 3 recent pending or failed tasks."""
        try:
            db = get_db()
            # We don't have a direct 'pending' filter in get_recent_tasks, so we fetch more and filter
            all_tasks = get_recent_tasks(db, limit=20)
            db.close()
            
            # Simple heuristic: recent tasks that were not successful or just raw input
            # For this demo, let's just take the last 3 user inputs as "context" or "tasks"
            # In a real app, we'd query a proper Todo table.
            # Using recent tasks as a proxy.
            
            pending = []
            for t in all_tasks:
                if not t.success: # Failed tasks need attention
                    pending.append(t.user_input)
            
            # If not enough failed tasks, add recent ones
            if len(pending) < 3:
                for t in all_tasks:
                    if t.user_input not in pending:
                         pending.append(t.user_input)
            
            return pending[:3]
        except Exception as e:
            print(f"Task Fetch Error: {e}")
            return []

    async def _generate_greeting(self, date: str, weather: Dict, task_count: int) -> Dict[str, str]:
        """Ask Ollama for a personalized greeting and quote."""
        prompt = f"""
        Generate a JSON response for a morning briefing.
        Context:
        - Date: {date}
        - Weather: {weather['temp']}°C, {weather['condition']}
        - Pending Tasks: {task_count}
        
        Return JSON ONLY:
        {{
            "greeting": "A warm, energetic 2-sentence morning greeting mentioning the weather.",
            "quote": "A short, powerful motivational quote for productivity."
        }}
        """
        
        try:
            # We use chat method directly to avoid the tool-use structure of .plan()
            response_text = await self.ollama.chat([{"role": "user", "content": prompt}])
            
            # Try to parse JSON from the response
            import json
            import re
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"Greeting Gen Error: {e}")
            
        return {
            "greeting": f"Good morning! It's {weather['temp']}°C and {weather['condition']} today.",
            "quote": "The secret of getting ahead is getting started."
        }

    def format_text(self, data: Dict[str, Any]) -> str:
        """Format the briefing data into a speakable script."""
        script = f"{data['greeting']} Today is {data['date']}."
        
        if data['tasks']:
            script += f" You have some recent items to look at: {', '.join(data['tasks'])}."
        else:
            script += " You are all caught up on tasks."
            
        script += f" Remember: {data['quote']}"
        return script

# Global Instance
briefing = DailyBriefing()
