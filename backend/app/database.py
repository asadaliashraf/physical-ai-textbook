import asyncpg
from app.config import settings
from typing import Optional

_pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            settings.DATABASE_URL,
            min_size=2,
            max_size=10
        )
    return _pool

async def init_db():
    """Initialize database tables"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Users table
        await conn.execute("""
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

        # Chat history table
        await conn.execute("""
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

        # Reading progress table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reading_progress (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                chapter_id VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                last_read TIMESTAMP DEFAULT NOW(),
                UNIQUE(user_id, chapter_id)
            )
        """)

        # Translations cache table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS translation_cache (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                chapter_id VARCHAR(255) NOT NULL,
                language VARCHAR(10) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(chapter_id, language)
            )
        """)

        print("Database initialized successfully!")

async def close_db():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
