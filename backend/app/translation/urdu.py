"""Urdu Translation using Gemini AI"""
import google.generativeai as genai
from app.config import settings
from app.database import get_pool
import re

genai.configure(api_key=settings.GEMINI_API_KEY)

TRANSLATION_PROMPT = """You are an expert technical translator specializing in translating
robotics and AI educational content from English to Urdu.

Rules:
1. Translate ALL text to Urdu (اردو)
2. Keep ALL code blocks exactly as-is (do not translate code)
3. Keep technical terms in English but add Urdu explanation in parentheses
4. Preserve markdown formatting (headings, bold, lists)
5. Make the translation natural and educational
6. Keep file paths, URLs, and command names in English
7. Keep module names and package names in English

Example:
English: "A **node** is an independent process that performs specific computations."
Urdu: "ایک **نوڈ** (Node) ایک آزاد عمل (Independent Process) ہے جو مخصوص حسابات انجام دیتا ہے۔"
"""

def extract_code_blocks(markdown: str) -> tuple[str, list[str]]:
    """Extract code blocks to protect from translation"""
    code_blocks = []
    placeholder_markdown = markdown

    def replace_code(match):
        code_blocks.append(match.group(0))
        return f"CODE_BLOCK_{len(code_blocks) - 1}_PLACEHOLDER"

    placeholder_markdown = re.sub(r'```[\s\S]*?```', replace_code, placeholder_markdown)
    return placeholder_markdown, code_blocks

def restore_code_blocks(text: str, code_blocks: list[str]) -> str:
    """Restore code blocks after translation"""
    for i, block in enumerate(code_blocks):
        text = text.replace(f"CODE_BLOCK_{i}_PLACEHOLDER", block)
    return text

async def translate_to_urdu(content: str, chapter_id: str) -> str:
    """Translate chapter content to Urdu, with caching"""
    # Check cache first
    pool = await get_pool()
    async with pool.acquire() as conn:
        cached = await conn.fetchrow(
            "SELECT content FROM translation_cache WHERE chapter_id = $1 AND language = 'ur'",
            chapter_id
        )
        if cached:
            return cached["content"]

    # Extract code blocks before translation
    placeholder_text, code_blocks = extract_code_blocks(content)

    # Translate in chunks (Gemini has context limits)
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={"temperature": 0.3, "max_output_tokens": 4096}
    )

    chunk_size = 3000
    translated_chunks = []

    for i in range(0, len(placeholder_text), chunk_size):
        chunk = placeholder_text[i:i+chunk_size]
        prompt = f"{TRANSLATION_PROMPT}\n\nTranslate the following to Urdu:\n\n{chunk}"

        response = model.generate_content(prompt)
        translated_chunks.append(response.text)

    translated = "".join(translated_chunks)

    # Restore code blocks
    translated = restore_code_blocks(translated, code_blocks)

    # Cache the translation
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO translation_cache (chapter_id, language, content)
               VALUES ($1, 'ur', $2)
               ON CONFLICT (chapter_id, language) DO UPDATE SET content = $2""",
            chapter_id, translated
        )

    return translated

async def translate_text(text: str, target_language: str = "ur") -> str:
    """Translate a short text snippet"""
    if target_language == "ur":
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Translate to Urdu (keep technical terms in English): {text}"
        )
        return response.text
    return text
