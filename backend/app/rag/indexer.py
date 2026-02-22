"""Index all textbook content into Qdrant"""
import os
import re
import glob
from pathlib import Path
from app.rag.embeddings import get_embedding
from app.rag.vector_store import upsert_documents, init_collection

DOCS_DIR = Path(__file__).parent.parent.parent.parent / "docs"
CHUNK_SIZE = 800  # characters per chunk
CHUNK_OVERLAP = 100

def clean_markdown(text: str) -> str:
    """Remove markdown syntax for better embedding"""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`[^`]*`', '', text)
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove bold/italic
    text = re.sub(r'\*\*?([^*]+)\*\*?', r'\1', text)
    # Remove frontmatter
    text = re.sub(r'^---[\s\S]*?---\n', '', text)
    # Clean whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        chunks.append(text[start:end])
        start = end - overlap
        if start >= len(text):
            break
    return chunks

def get_chapter_info(file_path: str) -> dict:
    """Extract chapter metadata from file path and content"""
    path = Path(file_path)
    parts = path.parts

    # Extract module number
    module = ""
    for part in parts:
        if part.startswith("module-"):
            module = part

    # Read frontmatter for title
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else path.stem

    chapter_id = f"{module}/{path.stem}" if module else path.stem

    return {
        "chapter_id": chapter_id,
        "chapter_title": title,
        "module": module,
        "file_path": file_path
    }

async def index_all_docs():
    """Index all markdown documents into Qdrant"""
    await init_collection()

    # Find all markdown files
    md_files = glob.glob(str(DOCS_DIR / "**" / "*.md"), recursive=True)
    print(f"Found {len(md_files)} documents to index")

    all_documents = []
    all_embeddings = []

    for file_path in md_files:
        try:
            chapter_info = get_chapter_info(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            clean_content = clean_markdown(raw_content)
            if len(clean_content) < 100:
                continue

            chunks = chunk_text(clean_content)
            print(f"Indexing: {chapter_info['chapter_title']} ({len(chunks)} chunks)")

            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) < 50:
                    continue

                embedding = await get_embedding(chunk)
                all_documents.append({
                    "content": chunk,
                    "chapter_id": chapter_info["chapter_id"],
                    "chapter_title": chapter_info["chapter_title"],
                    "module": chapter_info["module"],
                    "chunk_index": i
                })
                all_embeddings.append(embedding)

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    # Batch upsert to Qdrant
    if all_documents:
        batch_size = 50
        for i in range(0, len(all_documents), batch_size):
            batch_docs = all_documents[i:i+batch_size]
            batch_embeddings = all_embeddings[i:i+batch_size]
            await upsert_documents(batch_docs, batch_embeddings)

    print(f"Indexed {len(all_documents)} chunks from {len(md_files)} documents")
    return len(all_documents)
