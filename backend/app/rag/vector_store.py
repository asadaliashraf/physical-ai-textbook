"""Qdrant Vector Store for RAG system"""
from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
    SearchRequest
)
from app.config import settings
from typing import Optional
import uuid

# Gemini embedding dimension
EMBEDDING_DIM = 768

_client: Optional[AsyncQdrantClient] = None

async def get_client() -> AsyncQdrantClient:
    global _client
    if _client is None:
        if settings.QDRANT_URL:
            _client = AsyncQdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
        else:
            # Use in-memory for development
            _client = AsyncQdrantClient(":memory:")
    return _client

async def init_collection():
    """Create the collection if it doesn't exist"""
    client = await get_client()
    collections = await client.get_collections()
    collection_names = [c.name for c in collections.collections]

    if settings.QDRANT_COLLECTION not in collection_names:
        await client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )
        print(f"Created collection: {settings.QDRANT_COLLECTION}")

async def upsert_documents(documents: list[dict], embeddings: list[list[float]]):
    """Store documents with their embeddings"""
    client = await get_client()
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": doc["content"],
                "chapter_id": doc.get("chapter_id", ""),
                "chapter_title": doc.get("chapter_title", ""),
                "module": doc.get("module", ""),
                "chunk_index": doc.get("chunk_index", 0),
            }
        )
        for doc, embedding in zip(documents, embeddings)
    ]

    await client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points
    )
    print(f"Stored {len(points)} document chunks")

async def search(query_embedding: list[float], limit: int = 5, chapter_id: Optional[str] = None):
    """Search for relevant documents"""
    client = await get_client()

    # Optionally filter by chapter
    search_filter = None
    if chapter_id:
        search_filter = Filter(
            must=[FieldCondition(
                key="chapter_id",
                match=MatchValue(value=chapter_id)
            )]
        )

    results = await client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_embedding,
        query_filter=search_filter,
        limit=limit,
        with_payload=True
    )

    return [
        {
            "content": r.payload["content"],
            "chapter_id": r.payload.get("chapter_id", ""),
            "chapter_title": r.payload.get("chapter_title", ""),
            "score": r.score
        }
        for r in results
    ]
