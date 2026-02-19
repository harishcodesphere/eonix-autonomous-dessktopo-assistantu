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

    id           = Column(Integer, primary_key=True)
    name         = Column(String(100), unique=True)
    trigger_type = Column(String(20), default="manual") # manual, cron, event
    schedule     = Column(String(100), nullable=True)   # cron expression
    event_name   = Column(String(100), nullable=True)   # if trigger_type=event
    workflow_json= Column(Text)                         # JSON blob of nodes/edges
    active       = Column(Boolean, default=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    run_count    = Column(Integer, default=0)


class ConversationModel(Base):
    """Episodic memory: Full conversation history."""
    __tablename__ = "conversations"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    user_input  = Column(Text, nullable=False)
    agent_reply = Column(Text, nullable=False)
    tags        = Column(JSON)  # e.g. ["planning", "python"]
    embedding_id = Column(String(50), nullable=True) # Link to semantic DB if needed


class AppUsage(Base):
    """App usage tracking — one row per active-window session."""
    __tablename__ = "app_usage"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    app_name         = Column(String(200), nullable=False)
    window_title     = Column(Text, default="")
    start_time       = Column(DateTime, nullable=False)
    end_time         = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, default=0)
    date             = Column(String(10), nullable=False)  # YYYY-MM-DD for easy grouping
class SecurityLog(Base):
    """Security alerts and events."""
    __tablename__ = "security_log"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    severity    = Column(String(20), nullable=False)  # INFO, WARNING, CRITICAL
    category    = Column(String(50), nullable=False)   # network, process, port, privilege, device
    title       = Column(String(200), nullable=False)
    message     = Column(Text, default="")
    process_name = Column(String(200), nullable=True)
    pid         = Column(Integer, nullable=True)
    resolved    = Column(Boolean, default=False)
    date        = Column(String(10), nullable=False)


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
