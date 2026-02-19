"""
EONIX System Info — CPU, RAM, disk, battery, process monitoring.
"""
import psutil
import platform
import socket
from typing import Dict, List, Optional, Any


# Fallback definition used when running this module directly (outside the package)
class ToolResult:
    """Minimal stand-in used only when the real ToolResult cannot be imported."""
    def __init__(self, success: bool, message: str, data: Any = None) -> None:
        self.success = success
        self.message = message
        self.data = data

try:
    from tools.tool_result import ToolResult  # type: ignore[no-redef]  # overrides stub above
except ImportError:
    pass  # Keep the fallback class defined above

class SystemInfo:
    name = "get_system_info"
    description = "Gets real-time system metrics: CPU, RAM, disk, battery, processes"

    def get_cpu(self) -> Dict[str, Any]:
        try:
            freq = psutil.cpu_freq()
            return {
                "percent": psutil.cpu_percent(interval=1),
                "cores": psutil.cpu_count(logical=True),
                "physical_cores": psutil.cpu_count(logical=False),
                "freq_mhz": round(freq.current, 0) if freq else 0
            }
        except Exception as e:
            return {"error": f"CPU error: {e}"}

    def get_memory(self) -> Dict[str, Any]:
        try:
            mem = psutil.virtual_memory()
            return {
                "total_gb": round(mem.total / (1024**3), 2),
                "used_gb": round(mem.used / (1024**3), 2),
                "free_gb": round(mem.available / (1024**3), 2),
                "percent": mem.percent
            }
        except Exception as e:
            return {"error": f"Memory error: {e}"}

    def get_disk(self, path: str = "C:\\") -> Dict[str, Any]:
        try:
            disk = psutil.disk_usage(path)
            return {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            }
        except Exception:
            return {"error": f"Cannot access {path}"}

    def get_battery(self) -> Optional[Dict[str, Any]]:
        try:
            battery = psutil.sensors_battery()
            if not battery:
                return None
            return {
                "percent": round(battery.percent, 1),
                "plugged": battery.power_plugged,
                "minutes_left": round(battery.secsleft / 60, 0) if battery.secsleft > 0 else -1
            }
        except Exception:
            return None

    def get_processes(self, top_n: int = 15) -> List[Dict[str, Any]]:
        processes = []
        try:
            for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_info']):
                try:
                    info = proc.info
                    processes.append({
                        "name": info['name'],
                        "pid": info['pid'],
                        # cpu_percent can be None
                        "cpu_percent": info['cpu_percent'] or 0.0,
                        "memory_mb": round(info['memory_info'].rss / (1024**2), 1) if info.get('memory_info') else 0.0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            return []
            
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:top_n]  # type: ignore[index]

    def get_network(self) -> Dict[str, Any]:
        try:
            net = psutil.net_io_counters()
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return {
                "bytes_sent_mb": round(net.bytes_sent / (1024**2), 2),
                "bytes_recv_mb": round(net.bytes_recv / (1024**2), 2),
                "hostname": hostname,
                "ip": ip
            }
        except Exception as e:
            return {"error": str(e)}

    def get_all(self) -> Dict[str, Any]:
        data = {
            "cpu": self.get_cpu(),
            "memory": self.get_memory(),
            "disk": self.get_disk(),
            "network": self.get_network(),
            "platform": platform.system() + " " + platform.release()
        }
        battery = self.get_battery()
        if battery:
            data["battery"] = battery
        return data

    def execute(self, info_type: str = "all") -> ToolResult:
        """Universal system info dispatcher."""
        info_type = info_type.lower()
        msg = ""
        data: Dict[str, Any] = {}
        
        try:
            if info_type == "cpu":
                data = self.get_cpu()
                msg = f"CPU: {data.get('percent', 0)}% usage, {data.get('cores', '?')} cores"
            elif info_type in ["memory", "ram"]:
                data = self.get_memory()
                msg = f"RAM: {data.get('used_gb', '?')}GB used of {data.get('total_gb', '?')}GB ({data.get('percent', 0)}%)"
            elif info_type == "disk":
                data = self.get_disk()
                msg = f"Disk C: {data.get('used_gb', '?')}GB used of {data.get('total_gb', '?')}GB ({data.get('percent', 0)}%)"
            elif info_type == "battery":
                battery_data = self.get_battery()
                if battery_data is not None:
                    data = battery_data
                    status = "plugged in" if data.get('plugged') else "on battery"
                    msg = f"Battery: {data.get('percent', '?')}% ({status})"
                else:
                    data = {}
                    msg = "No battery detected (desktop PC)"
            elif info_type == "processes":
                procs = self.get_processes()
                data = {"processes": procs}
                msg = f"Top {len(procs)} processes by CPU usage"
            elif info_type == "network":
                data = self.get_network()
                msg = f"IP: {data.get('ip', 'unknown')}"
            else:
                data = self.get_all()
                cpu = data.get('cpu', {})
                mem = data.get('memory', {})
                msg = f"CPU: {cpu.get('percent', '?')}% | RAM: {mem.get('used_gb', '?')}GB used"

            return ToolResult(success=True, message=msg, data=data)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to get {info_type} info: {str(e)}")

# Global instance
system_info = SystemInfo()
