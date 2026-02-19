"""
Eonix General Helper Utilities
"""
import os
import time
import platform
from datetime import datetime
from typing import Any, Dict


def get_system_info() -> Dict[str, str]:
    """Get basic system information."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
    }


def format_bytes(size_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {units[i]}"


def format_uptime(seconds: float) -> str:
    """Convert seconds to human-readable uptime string."""
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


def timestamp_now() -> str:
    """Current UTC timestamp as ISO string."""
    return datetime.utcnow().isoformat()


def safe_json_serialize(obj: Any) -> Any:
    """Make an object JSON-serializable."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def ensure_directory(path: str) -> str:
    """Ensure a directory exists, create if not."""
    os.makedirs(path, exist_ok=True)
    return path
