"""
EONIX Semantic Memory — Long-term storage for facts and concepts using ChromaDB.
"""
import chromadb
import uuid
import os

class SemanticMemory:
    def __init__(self):
        # Persistent storage in ./data/chroma
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma")
        os.makedirs(self.db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Collection for general facts about the user
        self.collection = self.client.get_or_create_collection(
            name="user_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

    def store_fact(self, text: str, metadata: dict = None) -> str:
        """Store a semantic fact."""
        fact_id = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[fact_id]
        )
        return fact_id

    def retrieve_relevant(self, query: str, n_results: int = 3) -> list:
        """Retrieve most relevant facts for a query."""
        if self.collection.count() == 0:
            return []
            
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results: list of {"text": ..., "score": ...}
        memories = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                memories.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    # similarity score (lower distance = better match for some metrics, check chromadb)
                    "distance": results['distances'][0][i] if results['distances'] else 0
                })
        return memories

    def delete_fact(self, fact_id: str):
        self.collection.delete(ids=[fact_id])

    def get_all(self, limit: int = 20) -> list:
        """Get recent memories."""
        if self.collection.count() == 0:
            return []
        
        # Chroma .get doesn't support sorting by time easily without metadata
        # We just get the first N for now
        results = self.collection.get(limit=limit)
        return [
            {"id": id, "text": text, "metadata": meta}
            for id, text, meta in zip(results['ids'], results['documents'], results['metadatas'])
        ]

# Global instance
semantic_memory = SemanticMemory()
