"""
EONIX Memory API — Search and manage Episodic and Semantic memory.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from memory.episodic import episodic_memory
from memory.semantic import semantic_memory

router = APIRouter()

class FactRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class UserFactRequest(BaseModel):
    key: str
    value: str

@router.get("/search")
async def search_memory(q: str = Query(..., min_length=1), limit: int = 5):
    """Search episodic memory (conversations)."""
    episodic = episodic_memory.search(q, limit=limit)
    return {"episodic": episodic}

@router.get("/recent")
async def get_recent_episodic(limit: int = 10):
    """Get recent conversation history."""
    return episodic_memory.get_recent(limit=limit)

@router.get("/semantic/search")
async def search_semantic(q: str = Query(..., min_length=1), limit: int = 5):
    """Search semantic memory (facts)."""
    semantic = semantic_memory.retrieve_relevant(q, n_results=limit)
    return {"semantic": semantic}

@router.post("/fact")
async def add_fact(fact: FactRequest):
    """Manually add a fact to semantic memory."""
    fid = semantic_memory.store_fact(fact.text, fact.metadata)
    if not fid:
        raise HTTPException(status_code=500, detail="Failed to store fact")
    return {"status": "ok", "id": fid}

@router.post("/user_fact")
async def add_user_fact(fact: UserFactRequest):
    """Add a specific user key-value fact."""
    fid = semantic_memory.store_user_fact(fact.key, fact.value)
    if not fid:
        raise HTTPException(status_code=500, detail="Failed to store user fact")
    return {"status": "ok", "id": fid}

@router.delete("/{mem_id}")
async def delete_memory(mem_id: str, type: str = "semantic"):
    """Delete a memory item."""
    if type == "semantic":
        semantic_memory.delete_fact(mem_id)
        return {"status": "deleted"}
    else:
        # Episodic deletion not yet implemented in class, but API placeholder here
        raise HTTPException(status_code=501, detail="Episodic deletion not implemented")

@router.get("/all")
async def get_all_memories(limit: int = 50):
    """Get all memories (debug)."""
    return {
        "recent_episodic": episodic_memory.get_recent(limit),
        "semantic_facts": semantic_memory.get_all(limit)
    }
