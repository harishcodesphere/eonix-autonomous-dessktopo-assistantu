"""
EONIX System Info — CPU, RAM, disk, battery, process monitoring.
"""
import psutil
import platform
import socket
from .tool_result import ToolResult


class SystemInfo:
    name = "get_system_info"
    description = "Gets real-time system metrics: CPU, RAM, disk, battery, processes"

    def get_cpu(self) -> dict:
        freq = psutil.cpu_freq()
        return {
            "percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(logical=True),
            "physical_cores": psutil.cpu_count(logical=False),
            "freq_mhz": round(freq.current, 0) if freq else 0
        }

    def get_memory(self) -> dict:
        mem = psutil.virtual_memory()
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "free_gb": round(mem.available / (1024**3), 2),
            "percent": mem.percent
        }

    def get_disk(self, path: str = "C:\\") -> dict:
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

    def get_battery(self) -> dict | None:
        battery = psutil.sensors_battery()
        if not battery:
            return None
        return {
            "percent": round(battery.percent, 1),
            "plugged": battery.power_plugged,
            "minutes_left": round(battery.secsleft / 60, 0) if battery.secsleft > 0 else -1
        }

    def get_processes(self, top_n: int = 15) -> list:
        processes = []
        for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_info']):
            try:
                info = proc.info
                processes.append({
                    "name": info['name'],
                    "pid": info['pid'],
                    "cpu_percent": info['cpu_percent'] or 0,
                    "memory_mb": round(info['memory_info'].rss / (1024**2), 1) if info['memory_info'] else 0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:top_n]

    def get_network(self) -> dict:
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

    def get_all(self) -> dict:
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

    def kill_process(self, pid: int) -> ToolResult:
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.kill()
            return ToolResult(success=True, message=f"Killed process {name} (PID {pid})")
        except psutil.NoSuchProcess:
            return ToolResult(success=False, message=f"Process {pid} not found")
        except psutil.AccessDenied:
            return ToolResult(success=False, message=f"Access denied to kill process {pid}")
        except Exception as e:
            return ToolResult(success=False, message=f"Error: {str(e)}")

    def execute(self, info_type: str = "all") -> ToolResult:
        """Universal system info dispatcher."""
        info_type = info_type.lower()
        try:
            if info_type == "cpu":
                data = self.get_cpu()
                msg = f"CPU: {data['percent']}% usage, {data['cores']} cores"
            elif info_type == "memory" or info_type == "ram":
                data = self.get_memory()
                msg = f"RAM: {data['used_gb']}GB used of {data['total_gb']}GB ({data['percent']}%)"
            elif info_type == "disk":
                data = self.get_disk()
                msg = f"Disk C: {data['used_gb']}GB used of {data['total_gb']}GB ({data['percent']}%)"
            elif info_type == "battery":
                data = self.get_battery()
                if data:
                    status = "plugged in" if data['plugged'] else "on battery"
                    msg = f"Battery: {data['percent']}% ({status})"
                else:
                    data = {}
                    msg = "No battery detected (desktop PC)"
            elif info_type == "processes":
                data = {"processes": self.get_processes()}
                msg = f"Top {len(data['processes'])} processes by CPU usage"
            elif info_type == "network":
                data = self.get_network()
                msg = f"IP: {data.get('ip', 'unknown')}"
            else:
                data = self.get_all()
                cpu = data['cpu']
                mem = data['memory']
                msg = f"CPU: {cpu['percent']}% | RAM: {mem['used_gb']}GB/{mem['total_gb']}GB ({mem['percent']}%)"
            return ToolResult(success=True, message=msg, data=data)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to get {info_type} info: {str(e)}")
