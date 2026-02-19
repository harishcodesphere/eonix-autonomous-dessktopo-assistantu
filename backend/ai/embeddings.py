"""
Eonix Embeddings & Vector Store
Manages semantic embeddings via ChromaDB for memory and search.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from loguru import logger  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    import logging as _logging
    logger = _logging.getLogger(__name__)  # type: ignore[assignment]

try:
    import chromadb  # type: ignore[import-untyped]
    CHROMADB_AVAILABLE = True
except ImportError:  # pragma: no cover
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not installed. Vector search will be disabled.")


class EmbeddingManager:
    def __init__(self, persist_directory: str = "./data/chroma") -> None:
        self.persist_dir = persist_directory
        # Typed as Any so Pyright doesn't infer NoneType for every attribute access
        self.collection: Optional[Any] = None

        if CHROMADB_AVAILABLE:
            try:
                self.client: Any = chromadb.PersistentClient(path=self.persist_dir)
                self.collection = self.client.get_or_create_collection(
                    name="eonix_memory",
                    metadata={"hnsw:space": "cosine"},
                )
                logger.info(f"ChromaDB initialized at {self.persist_dir}")
            except Exception as e:
                logger.error(f"ChromaDB initialization failed: {e}")
                self.collection = None

    async def store(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store a text with its embedding in the vector DB."""
        if self.collection is None:
            return ""

        doc_id = str(uuid.uuid4())
        try:
            self.collection.add(
                documents=[text],
                metadatas=[{
                    **(metadata or {}),
                    "timestamp": datetime.utcnow().isoformat(),
                }],
                ids=[doc_id],
            )
            return doc_id
        except Exception as e:
            logger.error(f"Failed to store embedding: {e}")
            return ""

    async def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if self.collection is None:
            return []

        try:
            results: Dict[str, Any] = self.collection.query(
                query_texts=[query],
                n_results=n_results,
            )
            items: List[Dict[str, Any]] = []
            for i, doc in enumerate(results.get("documents", [[]])[0]):
                items.append({
                    "document": doc,
                    "metadata": results.get("metadatas", [[]])[0][i] if results.get("metadatas") else {},
                    "distance": results.get("distances", [[]])[0][i] if results.get("distances") else None,
                })
            return items
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    async def delete(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        if self.collection is None:
            return False
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception:
            return False
