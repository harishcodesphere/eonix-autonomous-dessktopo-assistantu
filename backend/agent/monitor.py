"""
System Monitor - Proactive health checks and alerts.
"""
import time
import asyncio
import psutil
import socket
from typing import Callable, Optional, Dict, List
from datetime import datetime

class SystemMonitor:
    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval
        self.running = False
        self.alert_callback: Optional[Callable[[Dict], None]] = None
        
        # State tracking for debouncing alerts
        self.cpu_high_count = 0
        self.last_alerts: Dict[str, float] = {}  # Type -> Timestamp

    def on_alert(self, callback: Callable[[Dict], None]):
        """Register a callback for sending alerts."""
        self.alert_callback = callback

    async def start(self):
        """Start the monitoring loop."""
        self.running = True
        print("System Monitor started.")
        while self.running:
            try:
                await self._check_all()
            except Exception as e:
                print(f"Monitor Error: {e}")
            
            # Sleep for interval
            for _ in range(self.check_interval):
                if not self.running: break
                await asyncio.sleep(1)

    def stop(self):
        """Stop the monitoring loop."""
        self.running = False
        print("System Monitor stopped.")

    async def _check_all(self):
        """Run all health checks."""
        # 1. CPU Check
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 85:
            self.cpu_high_count += 1
            if self.cpu_high_count >= 3:
                self._trigger_alert(
                    "High CPU Usage", 
                    "warning",
                    f"CPU is at {cpu_percent}%. System might be sluggish.",
                    "Close unused applications or check Task Manager."
                )
                self.cpu_high_count = 0 # Reset after alert
        else:
            self.cpu_high_count = 0

        # 2. Memory Check
        mem = psutil.virtual_memory()
        if mem.percent > 90:
            self._trigger_alert(
                "Low Memory",
                "critical",
                f"RAM is at {mem.percent}%.",
                "Close heavy applications (Chrome, Games) to free up memory."
            )

        # 3. Disk Check (C: drive)
        try:
            disk = psutil.disk_usage('C:\\')
            free_gb = disk.free / (1024 ** 3)
            if free_gb < 5:
                self._trigger_alert(
                    "Low Disk Space",
                    "warning",
                    f"Only {free_gb:.1f}GB free on C: drive.",
                    "Run 'Clean my disk' or empty Recycle Bin."
                )
        except Exception:
            pass # Ignore if C: checks fail

        # 4. Battery Check
        if psutil.sensors_battery():
            battery = psutil.sensors_battery()
            if battery and not battery.power_plugged and battery.percent < 15:
                self._trigger_alert(
                    "Battery Low",
                    "critical",
                    f"Battery at {battery.percent}% and discharging.",
                    "Plug in your charger immediately."
                )

        # 5. Internet Check (every 5th check to check less frequently, or just check every time if interval is 60s)
        # 60s is fine for simple ping
        if not self._check_internet():
             self._trigger_alert(
                "No Internet",
                "error",
                "System is offline.",
                "Check your Wi-Fi connection."
            )

    def _check_internet(self) -> bool:
        """Simple connectivity check."""
        try:
            # Connect to Google DNS
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def _trigger_alert(self, title: str, severity: str, message: str, suggestion: str):
        """Send alert if not recently sent (debounce)."""
        now = time.time()
        last_sent = self.last_alerts.get(title, 0)
        
        # Debounce: Don't send same alert within 10 minutes
        if now - last_sent < 600:
            return

        self.last_alerts[title] = now
        
        payload = {
            # "type": "system_alert", # Removed to let routes_ws.py set type="alert"
            "title": title,
            "severity": severity, # info, warning, error, critical
            "message": message,
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"SYS MONITOR ALERT: {title} - {message}")
        
        if self.alert_callback:
            # Prepare for broadcast
            # If callback is async, we should await it, but here we assume it handles it
            try:
                # We expect callback to be push_alert from main.py which is async
                # Since we are in async loop, we can create task
                asyncio.create_task(self.alert_callback(payload))
            except Exception as e:
                print(f"Failed to dispatch alert: {e}")

# Global instance
system_monitor = SystemMonitor()
