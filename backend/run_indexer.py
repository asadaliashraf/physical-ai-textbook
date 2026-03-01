import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

from app.rag.indexer import index_all_docs

async def main():
    print("Starting document indexing...")
    count = await index_all_docs()
    print(f"Done! Indexed {count} chunks.")

asyncio.run(main())
