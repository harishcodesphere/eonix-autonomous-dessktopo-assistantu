"""
EONIX Semantic Memory — Long-term storage for facts and concepts using ChromaDB.
"""
import uuid
import os
import time
from typing import Any, Dict, List, Optional

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMADB_AVAILABLE = True
except ImportError:
    chromadb = None  # type: ignore[assignment]
    CHROMADB_AVAILABLE = False

class SemanticMemory:
    def __init__(self) -> None:
        # Persistent storage in ./data/chroma
        self.db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma")
        os.makedirs(self.db_path, exist_ok=True)
        
        self.client: Any = None
        self.collection: Any = None
        self.is_fallback: bool = False
        self.fallback_memory: List[Dict[str, Any]] = []  # Simple list of dicts {text, metadata, id}

        if not CHROMADB_AVAILABLE:
            print("⚠️ SemanticMemory: chromadb module not found. Using in-memory fallback.")
            self.is_fallback = True
            return

        try:
            # Initialize Client
            if chromadb is not None:
                self.client = chromadb.PersistentClient(path=self.db_path)
            else:
                raise ImportError("chromadb is not available")
            
            # Initialize Collection
            self.collection = self.client.get_or_create_collection(
                name="user_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            print(f"✓ SemanticMemory: Connected to ChromaDB at {self.db_path}")
            
        except Exception as e:
            print(f"⚠️ SemanticMemory: ChromaDB init failed ({e}). Using in-memory fallback.")
            self.is_fallback = True
            self.client = None
            self.collection = None

    def store_fact(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store a semantic fact."""
        fact_id = str(uuid.uuid4())
        meta = metadata or {}
        # Ensure metadata values are strings/ints/floats (Chroma requirement)
        clean_meta: Dict[str, str] = {k: str(v) for k, v in meta.items()}
        
        if self.is_fallback or self.collection is None:
            self.fallback_memory.append({
                "id": fact_id,
                "text": text,
                "metadata": clean_meta,
                "timestamp": time.time()
            })
            return fact_id

        try:
            self.collection.add(
                documents=[text],
                metadatas=[clean_meta],
                ids=[fact_id]
            )
            return fact_id
        except Exception as e:
            print(f"❌ store_fact error: {e}")
            return ""

    def retrieve_relevant(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Retrieve most relevant facts for a query."""
        if self.is_fallback or self.collection is None:
            # Simple fallback: return last N items
            # (In a real fallback, we might do simple keyword matching)
            memories: List[Dict[str, Any]] = []
            query_words = query.split()
            # Filter by simple keyword match if possible
            matches = [
                m for m in self.fallback_memory 
                if any(w.lower() in str(m.get("text", "")).lower() for w in query_words)
            ]
            source = matches if matches else self.fallback_memory
            
            for m in reversed(source):
                if len(memories) >= n_results:
                    break
                memories.append({
                    "text": m.get("text", ""),
                    "metadata": m.get("metadata", {}),
                    "id": m.get("id", ""),
                    "distance": 0.5
                })
            return memories

        try:
            if self.collection.count() == 0:
                return []
                
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results: list of {"text": ..., "score": ...}
            memories = []
            if results and isinstance(results, dict) and results.get('documents'):
                # results['documents'] is list of list of strings
                docs = results.get('documents', [[]])[0]
                metas = results.get('metadatas', [[]])[0]
                ids = results.get('ids', [[]])[0]
                dists = results.get('distances', [[]])[0]
                
                for i in range(len(docs)):
                    memories.append({
                        "text": docs[i],
                        "metadata": metas[i] if i < len(metas) else {},
                        "id": ids[i] if i < len(ids) else "",
                        "distance": dists[i] if dists and i < len(dists) else 0
                    })
            return memories
            
        except Exception as e:
            print(f"❌ retrieve_relevant error: {e}")
            return []

    def delete_fact(self, fact_id: str) -> None:
        if self.is_fallback or self.collection is None:
            self.fallback_memory = [m for m in self.fallback_memory if m.get("id") != fact_id]
            return

        try:
            self.collection.delete(ids=[fact_id])
        except Exception as e:
            print(f"❌ delete_fact error: {e}")

    def get_all(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent memories."""
        if self.is_fallback or self.collection is None:
            all_items: List[Dict[str, Any]] = sorted(
                self.fallback_memory,
                key=lambda x: x.get("timestamp", 0),
                reverse=True
            )
            return all_items[0:limit] if len(all_items) > limit else all_items  # type: ignore[return-value]

        try:
            if self.collection.count() == 0:
                return []
            
            # Chroma .get()
            results = self.collection.get(limit=limit)
            # .get() returns:
            # {'ids': ['id1'], 'embeddings': None, 'documents': ['doc1'], 'metadatas': [{'k':'v'}]}
            
            memories: List[Dict[str, Any]] = []
            if not isinstance(results, dict):
                return []
            
            ids = results.get('ids', [])
            docs = results.get('documents', [])
            metas = results.get('metadatas', [])
            
            if docs is None:
                docs = []
            if ids is None:
                ids = []
            if metas is None:
                metas = []
            
            ids_list: List[Any] = list(ids) if ids else []
            metas_list: List[Any] = list(metas) if metas else []
            
            for i, doc in enumerate(docs):
                memories.append({
                    "id": ids_list[i] if i < len(ids_list) else "", 
                    "text": doc, 
                    "metadata": metas_list[i] if metas_list and i < len(metas_list) else {}
                })
            return memories
            
        except Exception as e:
            print(f"❌ get_all error: {e}")
            return []

# Global instance
semantic_memory = SemanticMemory()
