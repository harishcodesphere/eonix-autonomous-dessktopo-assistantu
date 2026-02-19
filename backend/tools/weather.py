"""
EONIX Weather Tool — Free weather data via wttr.in (no API key needed).
"""
import json
import urllib.request
import urllib.error
from tools.tool_result import ToolResult


class WeatherTool:
    name = "check_weather"
    description = "Get current weather for any city"

    def execute(self, city: str = "auto", **_) -> ToolResult:
        """Fetch weather for a city. Use 'auto' for IP-based location."""
        try:
            city_q = "" if city == "auto" else city.replace(" ", "+")
            url = f"https://wttr.in/{city_q}?format=j1"

            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            })
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            current = data["current_condition"][0]
            area = data.get("nearest_area", [{}])[0]
            city_name = area.get("areaName", [{}])[0].get("value", city)
            country = area.get("country", [{}])[0].get("value", "")

            temp_c = current.get("temp_C", "?")
            feels = current.get("FeelsLikeC", "?")
            desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
            humidity = current.get("humidity", "?")
            wind_kmph = current.get("windspeedKmph", "?")
            wind_dir = current.get("winddir16Point", "")

            msg = (
                f"🌤 Weather in {city_name}, {country}\n"
                f"  Temperature: {temp_c}°C (feels like {feels}°C)\n"
                f"  Condition: {desc}\n"
                f"  Humidity: {humidity}%\n"
                f"  Wind: {wind_kmph} km/h {wind_dir}"
            )

            return ToolResult(success=True, message=msg, data={
                "city": city_name,
                "country": country,
                "temp_c": temp_c,
                "feels_like_c": feels,
                "condition": desc,
                "humidity": humidity,
                "wind_kmph": wind_kmph,
            })

        except urllib.error.URLError as e:
            return ToolResult(success=False, message=f"Weather lookup failed (network): {e}")
        except Exception as e:
            return ToolResult(success=False, message=f"Weather lookup failed: {e}")
