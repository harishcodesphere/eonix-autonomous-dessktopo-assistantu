"""
EONIX Database Layer — SQLAlchemy ORM models and session management.
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Import DB_PATH safely
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import DB_PATH

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class Task(Base):
    """Every task/command the user has given, and its outcome."""
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    user_input  = Column(Text, nullable=False)
    brain_used  = Column(String(20))
    intent      = Column(String(100))
    plan        = Column(JSON)
    actions     = Column(JSON)
    result      = Column(Text)
    success     = Column(Boolean, default=None)
    duration_ms = Column(Integer)


class Preference(Base):
    """User preferences learned or explicitly set."""
    __tablename__ = "preferences"

    id         = Column(Integer, primary_key=True)
    key        = Column(String(100), unique=True)
    value      = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source     = Column(String(20), default="learned")


class AppAlias(Base):
    """Custom app name → executable mappings."""
    __tablename__ = "app_aliases"

    id     = Column(Integer, primary_key=True)
    alias  = Column(String(100), unique=True)
    exe    = Column(String(255))
    args   = Column(String(255), default="")


class Workflow(Base):
    """Saved multi-step workflows."""
    __tablename__ = "workflows"

    id          = Column(Integer, primary_key=True)
    name        = Column(String(100), unique=True)
    description = Column(Text)
    steps       = Column(JSON)
    created_at  = Column(DateTime, default=datetime.utcnow)
    run_count   = Column(Integer, default=0)


def init_db():
    """Create all tables."""
    Base.metadata.create_all(engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise
