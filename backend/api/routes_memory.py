"""
EONIX Memory API — Endpoints to store and retrieve semantic memories.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from memory.semantic import SemanticMemory

router = APIRouter()
memory_store = SemanticMemory()

class MemoryItem(BaseModel):
    text: str
    metadata: dict = {}

class MemorySearch(BaseModel):
    query: str
    limit: int = 3

@router.post("/memory/add")
async def add_memory(item: MemoryItem):
    """Store a new fact or memory."""
    try:
        fact_id = memory_store.store_fact(item.text, item.metadata)
        return {"status": "success", "id": fact_id, "message": "Memory stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/memory/search")
async def search_memory(search: MemorySearch):
    """Search for relevant memories."""
    try:
        results = memory_store.retrieve_relevant(search.query, search.limit)
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/memory/{fact_id}")
async def delete_memory(fact_id: str):
    """Delete a memory by ID."""
    try:
        memory_store.delete_fact(fact_id)
        return {"status": "success", "message": "Memory deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
