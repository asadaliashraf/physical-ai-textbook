"""RAG Retrieval and Generation using Gemini"""
import google.generativeai as genai
from app.config import settings
from app.rag.embeddings import get_query_embedding
from app.rag.vector_store import search
from typing import Optional, AsyncIterator

genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an intelligent AI tutor for a Physical AI & Humanoid Robotics textbook.
Your role is to help students understand complex robotics concepts clearly and accurately.

Guidelines:
- Answer questions based ONLY on the provided context from the textbook
- Use clear, educational language appropriate for the student's background
- Provide practical examples when explaining concepts
- If asked about code, explain what it does step by step
- If the answer is not in the provided context, say so honestly
- For Pakistani students, you can relate concepts to local examples when helpful

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

    # Build the actual query (include selected text if provided)
    if selected_text:
        full_query = f"Regarding this text: '{selected_text[:500]}'\n\nQuestion: {query}"
    else:
        full_query = query

    # Get relevant context from Qdrant
    query_embedding = await get_query_embedding(full_query)
    relevant_docs = await search(query_embedding, limit=5, chapter_id=chapter_id)

    if not relevant_docs:
        # Fallback: search without chapter filter
        relevant_docs = await search(query_embedding, limit=5)

    # Build context string
    context = ""
    sources = []
    for i, doc in enumerate(relevant_docs, 1):
        context += f"\n--- Source {i} ({doc['chapter_title']}) ---\n{doc['content']}\n"
        if doc['chapter_id'] not in sources:
            sources.append(doc['chapter_id'])

    # Personalize based on user background
    background_note = ""
    if user_background:
        exp = user_background.get("programming_experience", "beginner")
        goal = user_background.get("learning_goal", "overview")
        if exp == "none" or exp == "beginner":
            background_note = "\nNote: Explain at a beginner level with simple analogies."
        elif exp == "advanced":
            background_note = "\nNote: You can use technical terminology and advanced concepts."
        if goal == "project_based":
            background_note += " Focus on practical implementation."

    # Language instruction
    lang_instruction = ""
    if language == "urdu":
        lang_instruction = "\n\nIMPORTANT: Respond in Urdu (اردو) language."
    elif language == "both":
        lang_instruction = "\n\nProvide the response in both English and Urdu."

    # Build the final prompt
    prompt = f"""{SYSTEM_PROMPT}
{background_note}
{lang_instruction}

Context from the textbook:
{context}

Student's question: {full_query}

Please provide a clear, helpful answer based on the context above:"""

    # Generate streaming response with Gemini
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={"temperature": 0.7, "max_output_tokens": 1024}
    )

    # Add conversation history if provided
    history = []
    if conversation_history:
        for msg in conversation_history[-6:]:  # Last 3 exchanges
            history.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })

    chat = model.start_chat(history=history)
    response = chat.send_message(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            yield chunk.text

    # Yield sources at the end
    if sources:
        yield f"\n\n---\n📚 **Sources**: {', '.join(sources)}"
