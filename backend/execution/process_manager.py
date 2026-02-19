import psutil
from typing import List, Dict
from loguru import logger

class ProcessManager:
    @staticmethod
    def get_processes() -> List[Dict]:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    @staticmethod
    def kill_process(pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except Exception as e:
            logger.error(f"Error killing process {pid}: {e}")
            return False

    @staticmethod
    def get_system_metrics() -> Dict:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict()
        }
