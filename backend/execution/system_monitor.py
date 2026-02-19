"""
Eonix System Monitor
Real-time system resource monitoring with history tracking.
"""
import asyncio
import time
import psutil
from typing import Dict, List
from loguru import logger


class SystemMonitor:
    """Monitors system resources and maintains a rolling history."""

    def __init__(self, history_size: int = 60):
        self.history_size = history_size
        self.cpu_history: List[float] = []
        self.memory_history: List[float] = []
        self.timestamps: List[float] = []
        self._running = False
        self._task = None

    async def start(self):
        """Start background monitoring."""
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("System monitor started")

    async def stop(self):
        """Stop background monitoring."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("System monitor stopped")

    async def _monitor_loop(self):
        """Background loop that collects metrics every 2 seconds."""
        while self._running:
            try:
                cpu = psutil.cpu_percent(interval=0)
                mem = psutil.virtual_memory().percent

                self.cpu_history.append(cpu)
                self.memory_history.append(mem)
                self.timestamps.append(time.time())

                # Trim to history size
                if len(self.cpu_history) > self.history_size:
                    self.cpu_history = self.cpu_history[-self.history_size:]
                    self.memory_history = self.memory_history[-self.history_size:]
                    self.timestamps = self.timestamps[-self.history_size:]

                await asyncio.sleep(2)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(5)

    async def get_stats(self) -> Dict:
        """Get current system statistics."""
        try:
            cpu_freq = psutil.cpu_freq()
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/") if psutil.LINUX or psutil.MACOS else psutil.disk_usage("C:\\")
            net = psutil.net_io_counters()

            stats = {
                "cpu": {
                    "percent": psutil.cpu_percent(interval=0),
                    "per_core": psutil.cpu_percent(interval=0, percpu=True),
                    "cores": psutil.cpu_count(logical=True),
                    "frequency_mhz": cpu_freq.current if cpu_freq else 0,
                },
                "memory": {
                    "total_gb": round(mem.total / (1024 ** 3), 1),
                    "used_gb": round(mem.used / (1024 ** 3), 1),
                    "available_gb": round(mem.available / (1024 ** 3), 1),
                    "percent": mem.percent,
                },
                "disk": {
                    "total_gb": round(disk.total / (1024 ** 3), 1),
                    "used_gb": round(disk.used / (1024 ** 3), 1),
                    "free_gb": round(disk.free / (1024 ** 3), 1),
                    "percent": round(disk.percent, 1),
                },
                "network": {
                    "bytes_sent": net.bytes_sent,
                    "bytes_recv": net.bytes_recv,
                },
                "history": {
                    "cpu": self.cpu_history[-30:],
                    "memory": self.memory_history[-30:],
                },
            }

            # Battery info (laptops)
            battery = psutil.sensors_battery()
            if battery:
                stats["battery"] = {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged,
                    "secs_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else -1,
                }

            return stats

        except Exception as e:
            logger.error(f"Failed to get system stats: {e}")
            return {"error": str(e)}
