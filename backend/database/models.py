from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import datetime
from config import settings

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True)
    user_input = Column(Text)
    ai_response = Column(Text)
    intent = Column(String(50))
    metadata_json = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    definition = Column(JSON)
    description = Column(Text)

async def init_db():
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine
