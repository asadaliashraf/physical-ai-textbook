"""Gemini Embeddings via direct REST API (no SDK needed)"""
import httpx
from app.config import settings

GEMINI_EMBED_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent"

async def get_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{GEMINI_EMBED_URL}?key={settings.GEMINI_API_KEY}",
            json={
                "model": "models/gemini-embedding-001",
                "content": {"parts": [{"text": text}]},
                "taskType": task_type,
                "outputDimensionality": 768
            }
        )
        resp.raise_for_status()
        return resp.json()["embedding"]["values"]

async def get_query_embedding(query: str) -> list[float]:
    return await get_embedding(query, task_type="RETRIEVAL_QUERY")
