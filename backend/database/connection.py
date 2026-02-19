"""
Eonix Database Connection
Async SQLAlchemy engine and session management.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings
from loguru import logger


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Dependency injection for async database sessions."""
    async with async_session() as session:
        yield session


async def init_database():
    """Initialize database — create all tables."""
    from database.models import Base as ModelsBase  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(ModelsBase.metadata.create_all)
    logger.info("Database initialized successfully")


async def close_database():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")
