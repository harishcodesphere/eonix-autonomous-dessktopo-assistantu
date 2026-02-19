"""
Eonix Logging Configuration
Uses loguru for structured, colorful logging.
"""
import sys
import os
from loguru import logger

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Remove default handler
logger.remove()

# Console handler with color
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)

# File handler — main log
logger.add(
    os.path.join(LOG_DIR, "eonix.log"),
    rotation="10 MB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
)

# File handler — errors only
logger.add(
    os.path.join(LOG_DIR, "error.log"),
    rotation="10 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
)


def get_logger(name: str):
    """Get a named logger instance."""
    return logger.bind(name=name)
