"""
EONIX Proactive Monitor — Background intelligence loop.
Monitors system health and pushes alerts via WebSocket.
"""
import asyncio
import psutil
import time
from datetime import datetime
from typing import List, Dict, Callable

class SystemMonitor:
    """Background monitor that checks system health every 60 seconds."""

    def __init__(self):
        self.running = False
        self.alert_callbacks: List[Callable] = []
        self.check_interval = 60  # seconds
        
        # Thresholds
        self.cpu_threshold = 85       # %
        self.cpu_sustained_secs = 180 # 3 minutes
        self.ram_threshold = 90       # %
        self.disk_threshold_gb = 5    # GB free
        self.battery_threshold = 15   # %
        
        # State tracking
        self._cpu_high_since = None
        self._alerts_sent = set()  # Avoid spamming same alert

    def on_alert(self, callback: Callable):
        """Register a callback for alerts."""
        self.alert_callbacks.append(callback)

    async def _emit_alert(self, alert: Dict):
        """Send alert to all registered callbacks."""
        for cb in self.alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(alert)
                else:
                    cb(alert)
            except Exception as e:
                print(f"Alert callback error: {e}")

    async def check_once(self) -> List[Dict]:
        """Run a single health check and return any alerts."""
        alerts = []
        now = datetime.now().isoformat()

        # ── CPU Check ──
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.cpu_threshold:
            if self._cpu_high_since is None:
                self._cpu_high_since = time.time()
            elif time.time() - self._cpu_high_since > self.cpu_sustained_secs:
                alert_key = "cpu_sustained"
                if alert_key not in self._alerts_sent:
                    # Find top CPU processes
                    top_procs = []
                    for proc in psutil.process_iter(['name', 'cpu_percent']):
                        try:
                            if proc.info['cpu_percent'] > 10:
                                top_procs.append(f"{proc.info['name']} ({proc.info['cpu_percent']}%)")
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    alerts.append({
                        "type": "warning",
                        "category": "cpu",
                        "title": "CPU Running Hot 🔥",
                        "message": f"CPU at {cpu_percent}% for 3+ minutes. Top: {', '.join(top_procs[:3]) or 'unknown'}",
                        "timestamp": now,
                        "suggestion": "Consider closing heavy applications."
                    })
                    self._alerts_sent.add(alert_key)
        else:
            self._cpu_high_since = None
            self._alerts_sent.discard("cpu_sustained")

        # ── RAM Check ──
        ram = psutil.virtual_memory()
        if ram.percent > self.ram_threshold:
            alert_key = "ram_high"
            if alert_key not in self._alerts_sent:
                alerts.append({
                    "type": "warning",
                    "category": "ram",
                    "title": "Memory Running Low ⚠️",
                    "message": f"RAM at {ram.percent}% — {ram.available / (1024**3):.1f}GB free",
                    "timestamp": now,
                    "suggestion": "Close unused apps to free memory."
                })
                self._alerts_sent.add(alert_key)
        else:
            self._alerts_sent.discard("ram_high")

        # ── Disk Check ──
        disk = psutil.disk_usage('/')
        free_gb = disk.free / (1024**3)
        if free_gb < self.disk_threshold_gb:
            alert_key = "disk_low"
            if alert_key not in self._alerts_sent:
                alerts.append({
                    "type": "critical",
                    "category": "disk",
                    "title": "Disk Space Critical 💾",
                    "message": f"Only {free_gb:.1f}GB free on main drive!",
                    "timestamp": now,
                    "suggestion": "Run disk cleanup or delete temp files."
                })
                self._alerts_sent.add(alert_key)
        else:
            self._alerts_sent.discard("disk_low")

        # ── Battery Check ──
        battery = psutil.sensors_battery()
        if battery and not battery.power_plugged:
            if battery.percent < self.battery_threshold:
                alert_key = "battery_low"
                if alert_key not in self._alerts_sent:
                    alerts.append({
                        "type": "critical",
                        "category": "battery",
                        "title": "Battery Critical 🔋",
                        "message": f"Battery at {battery.percent}% and NOT charging!",
                        "timestamp": now,
                        "suggestion": "Plug in your charger immediately."
                    })
                    self._alerts_sent.add(alert_key)
            else:
                self._alerts_sent.discard("battery_low")

        return alerts

    async def start(self):
        """Start the background monitoring loop."""
        self.running = True
        print("🛡️ Proactive Monitor: ONLINE")
        while self.running:
            try:
                alerts = await self.check_once()
                for alert in alerts:
                    await self._emit_alert(alert)
            except Exception as e:
                print(f"Monitor error: {e}")
            await asyncio.sleep(self.check_interval)

    def stop(self):
        """Stop the monitoring loop."""
        self.running = False
        print("🛡️ Proactive Monitor: OFFLINE")


# Global instance
system_monitor = SystemMonitor()
