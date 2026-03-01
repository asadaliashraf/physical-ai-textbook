"""RAG Retrieval and Generation using Gemini REST API"""
import httpx
import json
from app.config import settings
from app.rag.embeddings import get_query_embedding
from app.rag.vector_store import search
from typing import Optional, AsyncIterator

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent"

SYSTEM_PROMPT = """You are an intelligent AI tutor for a Physical AI & Humanoid Robotics textbook.
Your role is to help students understand complex robotics concepts clearly and accurately.

Guidelines:
- Answer questions based ONLY on the provided context from the textbook
- Use clear, educational language appropriate for the student's background
- Provide practical examples when explaining concepts
- If asked about code, explain what it does step by step
- If the answer is not in the provided context, say so honestly

Always be encouraging and supportive in your teaching style."""

async def generate_rag_response(
    query: str,
    chapter_id: Optional[str] = None,
    selected_text: Optional[str] = None,
    user_background: Optional[dict] = None,
    conversation_history: Optional[list] = None,
    language: str = "english"
) -> AsyncIterator[str]:
    """Generate a streaming RAG response"""
    if selected_text:
        full_query = f"Regarding this text: '{selected_text[:500]}'\n\nQuestion: {query}"
    else:
        full_query = query

    # Get relevant context from Qdrant
    try:
        query_embedding = await get_query_embedding(full_query)
        relevant_docs = await search(query_embedding, limit=5, chapter_id=chapter_id)
        if not relevant_docs:
            relevant_docs = await search(query_embedding, limit=5)
    except Exception:
        relevant_docs = []

    # Build context
    context = ""
    sources = []
    for i, doc in enumerate(relevant_docs, 1):
        context += f"\n--- Source {i} ({doc['chapter_title']}) ---\n{doc['content']}\n"
        if doc['chapter_id'] not in sources:
            sources.append(doc['chapter_id'])

    # Personalization
    background_note = ""
    if user_background:
        exp = user_background.get("programming_experience", "beginner")
        if exp in ("none", "beginner"):
            background_note = "\nExplain at a beginner level with simple analogies."
        elif exp == "advanced":
            background_note = "\nUse technical terminology and advanced concepts."

    lang_instruction = ""
    if language == "urdu":
        lang_instruction = "\n\nIMPORTANT: Respond in Urdu (اردو) language."
    elif language == "both":
        lang_instruction = "\n\nProvide the response in both English and Urdu."

    prompt = f"""{SYSTEM_PROMPT}
{background_note}
{lang_instruction}

Context from the textbook:
{context}

Student's question: {full_query}

Please provide a clear, helpful answer based on the context above:"""

    # Build contents array (with optional history)
    contents = []
    if conversation_history:
        for msg in conversation_history[-6:]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    body = {
        "contents": contents,
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
    }

    # Stream response from Gemini
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream(
            "POST",
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}&alt=sse",
            json=body
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        candidates = data.get("candidates", [])
                        for candidate in candidates:
                            parts = candidate.get("content", {}).get("parts", [])
                            for part in parts:
                                text = part.get("text", "")
                                if text:
                                    yield text
                    except json.JSONDecodeError:
                        continue

    if sources:
        yield f"\n\n---\n**Sources**: {', '.join(sources)}"
