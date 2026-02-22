"""Gemini Embeddings for RAG system"""
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

async def get_embedding(text: str) -> list[float]:
    """Generate embedding for a text using Gemini"""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return result["embedding"]

async def get_query_embedding(query: str) -> list[float]:
    """Generate embedding for a search query"""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query"
    )
    return result["embedding"]
