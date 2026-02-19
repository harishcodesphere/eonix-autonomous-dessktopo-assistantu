"""
EONIX Episodic Memory — Stores full conversation history in SQLite.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import or_, desc
from memory.db import get_db, ConversationModel

class EpisodicMemory:
    def __init__(self):
        pass

    def save_turn(self, user_input: str, agent_reply: str, tags: Optional[List[str]] = None) -> int:
        """Save a conversation turn (User -> Agent)."""
        db = get_db()
        try:
            cleaned_tags = tags or []
            conversation = ConversationModel(
                user_input=user_input,
                agent_reply=agent_reply,
                tags=cleaned_tags,
                timestamp=datetime.utcnow()
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            return conversation.id
        except Exception as e:
            print(f"ERROR: Episodic Save Failed: {e}")
            db.rollback()
            return -1
        finally:
            db.close()

    def get_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent conversation turns."""
        db = get_db()
        try:
            turns = db.query(ConversationModel).order_by(desc(ConversationModel.timestamp)).limit(limit).all()
            # Reverse to return in chronological order (oldest -> newest) for context window
            return [
                {
                    "user": t.user_input,
                    "agent": t.agent_reply,
                    "timestamp": t.timestamp.isoformat(),
                    "tags": t.tags
                }
                for t in reversed(turns)
            ]
        except Exception as e:
            print(f"ERROR: Episodic Retrieve Failed: {e}")
            return []
        finally:
            db.close()

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search past conversations by keyword (SQL LIKE)."""
        # Note: comprehensive semantic search on conversations would require embedding every turn.
        # For now, we use SQL text search on user input.
        db = get_db()
        try:
            results = db.query(ConversationModel).filter(
                or_(
                    ConversationModel.user_input.ilike(f"%{query}%"),
                    ConversationModel.agent_reply.ilike(f"%{query}%")
                )
            ).order_by(desc(ConversationModel.timestamp)).limit(limit).all()
            
            return [
                {
                    "id": t.id,
                    "user": t.user_input,
                    "agent": t.agent_reply,
                    "timestamp": t.timestamp.isoformat()
                }
                for t in results
            ]
        except Exception as e:
            print(f"ERROR: Episodic Search Failed: {e}")
            return []
        finally:
            db.close()

# Global instance
episodic_memory = EpisodicMemory()
