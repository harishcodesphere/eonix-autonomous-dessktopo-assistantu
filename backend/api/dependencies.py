"""
Eonix API Dependencies
FastAPI dependency injection for database, auth, and services.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_session
from config import settings


async def get_db() -> AsyncSession:
    """Get an async database session."""
    async for session in get_session():
        yield session


async def verify_api_key(api_key: str = None):
    """Simple API key verification (optional, for remote access)."""
    if settings.SECRET_KEY and api_key:
        if api_key != settings.SECRET_KEY:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Invalid API key")
    return True
