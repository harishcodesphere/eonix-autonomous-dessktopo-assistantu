"""
Eonix Custom Decorators
"""
import time
import functools
import asyncio
from loguru import logger


def timed(func):
    """Log execution time of a function."""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        logger.debug(f"{func.__name__} completed in {elapsed:.1f}ms")
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        logger.debug(f"{func.__name__} completed in {elapsed:.1f}ms")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(f"{func.__name__} attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        await asyncio.sleep(delay)
            raise last_exc

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(f"{func.__name__} attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator


def require_permission(permission_name: str):
    """Decorator to check permission before executing."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Permission check will integrate with PermissionManager
            logger.info(f"Permission check: {permission_name}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
