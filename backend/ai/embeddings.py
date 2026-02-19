"""
Eonix Embeddings & Vector Store
Manages semantic embeddings via ChromaDB for memory and search.
"""
import uuid
from datetime import datetime
from loguru import logger

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not installed. Vector search will be disabled.")


class EmbeddingManager:
    def __init__(self, persist_directory: str = "./data/chroma"):
        self.persist_dir = persist_directory
        self.collection = None

        if CHROMADB_AVAILABLE:
            try:
                self.client = chromadb.PersistentClient(path=self.persist_dir)
                self.collection = self.client.get_or_create_collection(
                    name="eonix_memory",
                    metadata={"hnsw:space": "cosine"},
                )
                logger.info(f"ChromaDB initialized at {self.persist_dir}")
            except Exception as e:
                logger.error(f"ChromaDB initialization failed: {e}")
                self.collection = None

    async def store(self, text: str, metadata: dict = None) -> str:
        """Store a text with its embedding in the vector DB."""
        if not self.collection:
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

    async def search(self, query: str, n_results: int = 5) -> list[dict]:
        """Search for similar documents."""
        if not self.collection:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
            )
            items = []
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
        if not self.collection:
            return False
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception:
            return False
