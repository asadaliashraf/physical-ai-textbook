from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Gemini AI
    GEMINI_API_KEY: str = ""

    # Qdrant Vector DB
    QDRANT_URL: str = ""
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION: str = "physical_ai_textbook"

    # Neon Postgres Database
    DATABASE_URL: str = ""

    # JWT Auth
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://your-username.github.io",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

_settings = Settings()

# Strip whitespace from all string env vars (Vercel sometimes adds trailing newlines)
_settings.GEMINI_API_KEY = _settings.GEMINI_API_KEY.strip()
_settings.QDRANT_URL = _settings.QDRANT_URL.strip()
if _settings.QDRANT_API_KEY:
    _settings.QDRANT_API_KEY = _settings.QDRANT_API_KEY.strip()
_settings.DATABASE_URL = _settings.DATABASE_URL.strip()
_settings.SECRET_KEY = _settings.SECRET_KEY.strip()

settings = _settings
