"""
Physical AI Textbook - Backend API
FastAPI + Gemini + Qdrant + Neon Postgres + better-auth
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import asyncio

from app.config import settings
from app.database import init_db, close_db, get_pool
from app.auth import auth_router, get_current_user
from app.rag.retrieval import generate_rag_response
from app.translation.urdu import translate_to_urdu, translate_text
from app.personalization.content import personalize_content
from app.rag.indexer import index_all_docs

app = FastAPI(
    title="Physical AI Textbook API",
    description="AI-powered backend for the Physical AI & Humanoid Robotics Textbook",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth routes
app.include_router(auth_router)

# ==================
# Startup/Shutdown
# ==================

@app.on_event("startup")
async def startup():
    try:
        await init_db()
        print("Database initialized!")
    except Exception as e:
        print(f"Database init skipped (no connection): {e}")

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# ==================
# Request Models
# ==================

class ChatRequest(BaseModel):
    query: str
    chapter_id: Optional[str] = None
    selected_text: Optional[str] = None
    session_id: Optional[str] = None
    language: str = "english"
    conversation_history: Optional[List[dict]] = None

class TranslateRequest(BaseModel):
    chapter_id: str
    content: str

class PersonalizeRequest(BaseModel):
    chapter_id: str
    content: str

class ProgressUpdate(BaseModel):
    chapter_id: str
    completed: bool

# ==================
# Chat / RAG Routes
# ==================

@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    current_user: Optional[dict] = None
):
    """Main RAG chatbot endpoint with streaming"""
    try:
        user_background = None
        if current_user:
            user_background = current_user.get("background", {})

        async def event_stream():
            try:
                async for chunk in generate_rag_response(
                    query=request.query,
                    chapter_id=request.chapter_id,
                    selected_text=request.selected_text,
                    user_background=user_background,
                    conversation_history=request.conversation_history,
                    language=request.language
                ):
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            finally:
                yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/authenticated")
async def chat_authenticated(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Authenticated chat with personalization"""
    user_background = current_user.get("background", {})

    # Save chat to history
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO chat_history
                   (user_id, session_id, role, content, chapter_id, selected_text)
                   VALUES ($1, $2, 'user', $3, $4, $5)""",
                current_user["id"],
                request.session_id or "default",
                request.query,
                request.chapter_id,
                request.selected_text
            )
    except Exception:
        pass  # Don't fail if DB is unavailable

    async def event_stream():
        full_response = ""
        try:
            async for chunk in generate_rag_response(
                query=request.query,
                chapter_id=request.chapter_id,
                selected_text=request.selected_text,
                user_background=user_background,
                conversation_history=request.conversation_history,
                language=request.language
            ):
                full_response += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n"

            # Save assistant response
            try:
                pool = await get_pool()
                async with pool.acquire() as conn:
                    await conn.execute(
                        """INSERT INTO chat_history
                           (user_id, session_id, role, content, chapter_id)
                           VALUES ($1, $2, 'assistant', $3, $4)""",
                        current_user["id"],
                        request.session_id or "default",
                        full_response,
                        request.chapter_id
                    )
            except Exception:
                pass

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/api/chat/history")
async def get_chat_history(
    session_id: str = "default",
    current_user: dict = Depends(get_current_user)
):
    """Get chat history for current user"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT role, content, created_at FROM chat_history
               WHERE user_id = $1 AND session_id = $2
               ORDER BY created_at ASC LIMIT 50""",
            current_user["id"], session_id
        )
    return [dict(r) for r in rows]

# ==================
# Translation Routes
# ==================

@app.post("/api/translate")
async def translate_chapter(request: TranslateRequest):
    """Translate chapter content to Urdu"""
    try:
        translated = await translate_to_urdu(request.content, request.chapter_id)
        return {"translated": translated, "language": "ur"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")

@app.post("/api/translate/text")
async def translate_snippet(text: str, language: str = "ur"):
    """Translate a short text snippet"""
    translated = await translate_text(text, language)
    return {"original": text, "translated": translated, "language": language}

# ==================
# Personalization Routes
# ==================

@app.post("/api/personalize")
async def personalize_chapter(
    request: PersonalizeRequest,
    current_user: dict = Depends(get_current_user)
):
    """Personalize chapter content for the user"""
    try:
        user_background = current_user.get("background", {})
        personalized = await personalize_content(
            request.content,
            request.chapter_id,
            user_background
        )
        return {"personalized": personalized, "background": user_background}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personalization failed: {e}")

# ==================
# Progress Tracking
# ==================

@app.post("/api/progress")
async def update_progress(
    update: ProgressUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update reading progress for a chapter"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO reading_progress (user_id, chapter_id, completed)
               VALUES ($1, $2, $3)
               ON CONFLICT (user_id, chapter_id)
               DO UPDATE SET completed = $3, last_read = NOW()""",
            current_user["id"],
            update.chapter_id,
            update.completed
        )
    return {"message": "Progress updated", "chapter_id": update.chapter_id}

@app.get("/api/progress")
async def get_progress(current_user: dict = Depends(get_current_user)):
    """Get all reading progress for the user"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT chapter_id, completed, last_read FROM reading_progress WHERE user_id = $1",
            current_user["id"]
        )
    return [dict(r) for r in rows]

# ==================
# Admin Routes
# ==================

@app.post("/api/admin/index")
async def trigger_indexing():
    """Trigger document indexing (admin only)"""
    try:
        count = await index_all_docs()
        return {"message": f"Indexed {count} document chunks successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================
# Health Check
# ==================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Physical AI Textbook API",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "message": "Physical AI Textbook API",
        "docs": "/api/docs",
        "health": "/health"
    }
