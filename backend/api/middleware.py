"""
Eonix API Middleware
Custom middleware for logging, authentication, and rate limiting.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests with timing."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(
            f"{request.method} {request.url.path} — {response.status_code} ({elapsed:.0f}ms)"
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting (per IP)."""

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old entries
        if client_ip in self._requests:
            self._requests[client_ip] = [
                t for t in self._requests[client_ip] if now - t < self.window
            ]
        else:
            self._requests[client_ip] = []

        if len(self._requests[client_ip]) >= self.max_requests:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                {"detail": "Rate limit exceeded"}, status_code=429
            )

        self._requests[client_ip].append(now)
        return await call_next(request)
