"""Urdu Translation using Gemini REST API"""
import httpx
import re
from app.config import settings
from app.database import get_pool

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

TRANSLATION_PROMPT = """You are an expert technical translator specializing in translating
robotics and AI educational content from English to Urdu.

Rules:
1. Translate ALL text to Urdu (اردو)
2. Keep ALL code blocks exactly as-is (do not translate code)
3. Keep technical terms in English but add Urdu explanation in parentheses
4. Preserve markdown formatting (headings, bold, lists)
5. Make the translation natural and educational
6. Keep file paths, URLs, and command names in English"""

def extract_code_blocks(markdown: str) -> tuple[str, list[str]]:
    code_blocks = []
    def replace_code(match):
        code_blocks.append(match.group(0))
        return f"CODE_BLOCK_{len(code_blocks) - 1}_PLACEHOLDER"
    placeholder_markdown = re.sub(r'```[\s\S]*?```', replace_code, markdown)
    return placeholder_markdown, code_blocks

def restore_code_blocks(text: str, code_blocks: list[str]) -> str:
    for i, block in enumerate(code_blocks):
        text = text.replace(f"CODE_BLOCK_{i}_PLACEHOLDER", block)
    return text

async def _call_gemini(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.3, "maxOutputTokens": 4096}}
        )
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

async def translate_to_urdu(content: str, chapter_id: str) -> str:
    # Check cache first
    pool = await get_pool()
    async with pool.acquire() as conn:
        cached = await conn.fetchrow(
            "SELECT content FROM translation_cache WHERE chapter_id = $1 AND language = 'ur'",
            chapter_id
        )
        if cached:
            return cached["content"]

    placeholder_text, code_blocks = extract_code_blocks(content)
    chunk_size = 3000
    translated_chunks = []

    for i in range(0, len(placeholder_text), chunk_size):
        chunk = placeholder_text[i:i+chunk_size]
        prompt = f"{TRANSLATION_PROMPT}\n\nTranslate the following to Urdu:\n\n{chunk}"
        translated_chunks.append(await _call_gemini(prompt))

    translated = restore_code_blocks("".join(translated_chunks), code_blocks)

    # Cache it
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO translation_cache (chapter_id, language, content)
               VALUES ($1, 'ur', $2)
               ON CONFLICT (chapter_id, language) DO UPDATE SET content = $2""",
            chapter_id, translated
        )

    return translated

async def translate_text(text: str, target_language: str = "ur") -> str:
    if target_language == "ur":
        return await _call_gemini(f"Translate to Urdu (keep technical terms in English): {text}")
    return text
