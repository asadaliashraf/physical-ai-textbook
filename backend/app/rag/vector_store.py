"""Qdrant Vector Store via direct REST API (no SDK needed)"""
import httpx
import uuid
from app.config import settings
from typing import Optional

EMBEDDING_DIM = 768

def _headers():
    return {"api-key": settings.QDRANT_API_KEY, "Content-Type": "application/json"}

def _base():
    return settings.QDRANT_URL.rstrip("/")

async def init_collection():
    """Create the collection if it doesn't exist"""
    async with httpx.AsyncClient(timeout=30) as client:
        # Check if collection exists
        resp = await client.get(f"{_base()}/collections/{settings.QDRANT_COLLECTION}", headers=_headers())
        if resp.status_code == 200:
            return  # Already exists
        # Create it
        resp = await client.put(
            f"{_base()}/collections/{settings.QDRANT_COLLECTION}",
            headers=_headers(),
            json={"vectors": {"size": EMBEDDING_DIM, "distance": "Cosine"}}
        )
        resp.raise_for_status()
        print(f"Created Qdrant collection: {settings.QDRANT_COLLECTION}")

async def upsert_documents(documents: list[dict], embeddings: list[list[float]]):
    """Store documents with their embeddings"""
    points = [
        {
            "id": str(uuid.uuid4()),
            "vector": embedding,
            "payload": {
                "content": doc["content"],
                "chapter_id": doc.get("chapter_id", ""),
                "chapter_title": doc.get("chapter_title", ""),
                "module": doc.get("module", ""),
                "chunk_index": doc.get("chunk_index", 0),
            }
        }
        for doc, embedding in zip(documents, embeddings)
    ]
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.put(
            f"{_base()}/collections/{settings.QDRANT_COLLECTION}/points",
            headers=_headers(),
            json={"points": points}
        )
        resp.raise_for_status()
    print(f"Stored {len(points)} document chunks")

async def search(query_embedding: list[float], limit: int = 5, chapter_id: Optional[str] = None):
    """Search for relevant documents"""
    payload = {"vector": query_embedding, "limit": limit, "with_payload": True}
    if chapter_id:
        payload["filter"] = {"must": [{"key": "chapter_id", "match": {"value": chapter_id}}]}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{_base()}/collections/{settings.QDRANT_COLLECTION}/points/search",
            headers=_headers(),
            json=payload
        )
        resp.raise_for_status()
        results = resp.json().get("result", [])

    return [
        {
            "content": r["payload"]["content"],
            "chapter_id": r["payload"].get("chapter_id", ""),
            "chapter_title": r["payload"].get("chapter_title", ""),
            "score": r["score"]
        }
        for r in results
    ]
