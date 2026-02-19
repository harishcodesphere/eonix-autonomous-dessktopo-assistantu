"""
Eonix Long-Term Memory
Stores and retrieves interactions using vector embeddings for semantic search.
"""
from loguru import logger
from ai.embeddings import EmbeddingManager


class MemoryManager:
    """Long-term memory backed by vector database."""

    def __init__(self):
        self.embeddings = EmbeddingManager()

    async def store_interaction(
        self, user_input: str, response: str, intent: dict = None, actions: list = None
    ):
        """Store an interaction in long-term memory."""
        text = f"User: {user_input}\nEonix: {response}"
        metadata = {
            "user_input": user_input,
            "response": response[:500],  # Truncate for metadata
            "intent": intent.get("intent", "unknown") if intent else "unknown",
        }
        doc_id = await self.embeddings.store(text, metadata)
        if doc_id:
            logger.debug(f"Stored interaction in memory: {doc_id}")

    async def recall(self, query: str, n_results: int = 5) -> list[dict]:
        """Search memory for relevant past interactions."""
        results = await self.embeddings.search(query, n_results=n_results)
        logger.debug(f"Memory recall returned {len(results)} results for: {query[:50]}")
        return results

    async def forget(self, doc_id: str) -> bool:
        """Remove a specific memory."""
        return await self.embeddings.delete(doc_id)
