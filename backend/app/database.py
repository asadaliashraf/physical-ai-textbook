import psycopg2
import psycopg2.extras
from app.config import settings
from typing import Optional
import asyncio
import re

_conn: Optional[psycopg2.extensions.connection] = None

def _get_conn():
    global _conn
    if _conn is None or _conn.closed:
        db_url = settings.DATABASE_URL.replace("&channel_binding=require", "").replace("?channel_binding=require&", "?")
        if "channel_binding=require" in db_url:
            db_url = db_url.replace("?channel_binding=require", "")
        _conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)
        _conn.autocommit = True
    return _conn

def _to_psycopg2(query):
    return re.sub(r'\$(\d+)', '%s', query)

def _execute_sync(query, *args):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(_to_psycopg2(query), args if args else None)
    cur.close()

def _fetch_sync(query, *args):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(_to_psycopg2(query), args if args else None)
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    return rows

def _fetchrow_sync(query, *args):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(_to_psycopg2(query), args if args else None)
    row = cur.fetchone()
    cur.close()
    return dict(row) if row else None

def _fetchval_sync(query, *args):
    row = _fetchrow_sync(query, *args)
    if row:
        return list(row.values())[0]
    return None

async def db_execute(query, *args):
    return await asyncio.to_thread(_execute_sync, query, *args)

async def db_fetch(query, *args):
    return await asyncio.to_thread(_fetch_sync, query, *args)

async def db_fetchrow(query, *args):
    return await asyncio.to_thread(_fetchrow_sync, query, *args)

async def db_fetchval(query, *args):
    return await asyncio.to_thread(_fetchval_sync, query, *args)

# Compatibility shim so existing code using get_pool() still works
async def get_pool():
    return PoolShim()

class PoolShim:
    def acquire(self):
        return ConnShim()

class ConnShim:
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass
    async def execute(self, q, *a):
        return await db_execute(q, *a)
    async def fetch(self, q, *a):
        return await db_fetch(q, *a)
    async def fetchrow(self, q, *a):
        return await db_fetchrow(q, *a)
    async def fetchval(self, q, *a):
        return await db_fetchval(q, *a)

async def init_db():
    def _init():
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                background JSONB DEFAULT '{}',
                preferences JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                session_id VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                chapter_id VARCHAR(255),
                selected_text TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reading_progress (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                chapter_id VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                last_read TIMESTAMP DEFAULT NOW(),
                UNIQUE(user_id, chapter_id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS translation_cache (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                chapter_id VARCHAR(255) NOT NULL,
                language VARCHAR(10) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(chapter_id, language)
            )
        """)
        cur.close()
        print("Database initialized!")
    await asyncio.to_thread(_init)

async def close_db():
    global _conn
    if _conn and not _conn.closed:
        _conn.close()
        _conn = None
