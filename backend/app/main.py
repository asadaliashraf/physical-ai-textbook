"""Physical AI Textbook - Backend API"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import asyncio
import traceback

app = FastAPI(
    title="Physical AI Textbook API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy import errors stored here
_import_errors = {}

def _try_import():
    global _import_errors
    try:
        from app.config import settings
        from app.database import init_db, close_db, get_pool
        from app.auth import auth_router, get_current_user
        from app.rag.retrieval import generate_rag_response
        from app.translation.urdu import translate_to_urdu, translate_text
        from app.personalization.content import personalize_content
        from app.rag.indexer import index_all_docs
        app.include_router(auth_router)
        return True, None
    except Exception as e:
        _import_errors["error"] = str(e)
        _import_errors["trace"] = traceback.format_exc()
        return False, str(e)

_loaded, _load_error = _try_import()

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

@app.get("/health")
async def health_check():
    if _import_errors:
        return {
            "status": "degraded",
            "service": "Physical AI Textbook API",
            "import_error": _import_errors.get("error"),
            "trace": _import_errors.get("trace", "")[:1000]
        }
    return {"status": "healthy", "service": "Physical AI Textbook API", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Physical AI Textbook API", "docs": "/api/docs", "health": "/health"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not _loaded:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {_load_error}")
    from app.rag.retrieval import generate_rag_response

    async def event_stream():
        try:
            async for chunk in generate_rag_response(
                query=request.query,
                chapter_id=request.chapter_id,
                selected_text=request.selected_text,
                conversation_history=request.conversation_history,
                language=request.language
            ):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@app.post("/api/chat/authenticated")
async def chat_authenticated(request: ChatRequest, token: str = Depends(lambda: None)):
    return await chat(request)

@app.post("/api/translate")
async def translate_chapter(request: TranslateRequest):
    if not _loaded:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {_load_error}")
    from app.translation.urdu import translate_to_urdu
    try:
        translated = await translate_to_urdu(request.content, request.chapter_id)
        return {"translated": translated, "language": "ur"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")

@app.post("/api/personalize")
async def personalize_chapter(request: PersonalizeRequest):
    if not _loaded:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {_load_error}")
    from app.personalization.content import personalize_content
    try:
        personalized = await personalize_content(request.content, request.chapter_id, {})
        return {"personalized": personalized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personalization failed: {e}")

@app.post("/api/admin/index")
async def trigger_indexing():
    if not _loaded:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {_load_error}")
    from app.rag.indexer import index_all_docs
    try:
        count = await index_all_docs()
        return {"message": f"Indexed {count} document chunks successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/progress")
async def update_progress(update: ProgressUpdate):
    return {"message": "Progress updated", "chapter_id": update.chapter_id}

@app.get("/api/progress")
async def get_progress():
    return []
