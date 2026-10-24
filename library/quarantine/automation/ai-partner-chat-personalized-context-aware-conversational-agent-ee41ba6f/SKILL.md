---
name: "ai-partner-chat"
description: "基于用户画像和向量化笔记提供个性化对话。当用户需要个性化交流、上下文感知的回应，或希望 AI 记住并引用其之前的想法和笔记时使用。"
---

# AI Partner Chat

## Overview
Provide personalized, context‑aware conversations by loading user and AI persona files, indexing markdown notes with embeddings, and retrieving relevant chunks during a chat.

## Prerequisites
1. **Create directory structure**
   ```bash
   mkdir -p config notes vector_db scripts
   ```
2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   ./venv/bin/pip install -r .claude/skills/ai-partner-chat/scripts/requirements.txt
   ```
3. **Copy persona templates** from `.claude/skills/ai-partner-chat/assets/` to `config/` and rename them to `user-persona.md` and `ai-persona.md`.
4. **Add your markdown notes** to the `notes/` directory.
5. **Initialize the vector database** by running the indexing script (see below).

## Core Workflow
### 1. Indexing Notes
Create `scripts/chunk_and_index.py` with the following skeleton:
```python
import sys
from pathlib import Path
from typing import List
sys.path.insert(0, str(Path(__file__).parent.parent / ".claude/skills/ai-partner-chat/scripts"))

from chunk_schema import Chunk, validate_chunk
from vector_indexer import VectorIndexer

def chunk_note_file(filepath: str) -> List[Chunk]:
    """Analyze the given note and return a list of Chunk objects.
    The implementation should inspect the file format (headings, dates, etc.)
    and produce chunks that conform to `chunk_schema.Chunk`.
    """
    # Example simple implementation – replace with AI‑generated logic as needed
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    # Very naive split by double newlines
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for i, part in enumerate(parts):
        chunk = {
            "content": part,
            "metadata": {
                "filename": Path(filepath).name,
                "filepath": str(Path(filepath).resolve()),
                "chunk_id": i,
                "chunk_type": "generic"
            }
        }
        validate_chunk(chunk)
        chunks.append(chunk)
    return chunks


def main():
    indexer = VectorIndexer(db_path="./vector_db")
    indexer.initialize_db()
    all_chunks = []
    for note_file in Path("./notes").rglob("*.md"):
        chunks = chunk_note_file(str(note_file))
        all_chunks.extend(chunks)
    indexer.index_chunks(all_chunks)

if __name__ == "__main__":
    main()
```
Run the script:
```bash
./venv/bin/python scripts/chunk_and_index.py
```
### 2. Conversational Retrieval
```python
from scripts.vector_utils import get_relevant_notes

relevant = get_relevant_notes(query=user_query, db_path="./vector_db", top_k=5)
```
Or via CLI:
```bash
python scripts/query_notes.py "What did I write about project X?" --top-k 5
```
Combine the retrieved notes with the persona files to construct a prompt for your LLM.

## Maintenance
- **Add new notes**: `python scripts/add_note.py /path/to/new_note.md`
- **Update personas**: edit `config/user-persona.md` or `config/ai-persona.md` and restart the conversation.
- **Re‑index**: `python scripts/init_vector_db.py ./notes --db-path ./vector_db`

## Technical Details
- **Vector store**: ChromaDB persisted in `vector_db/`
- **Embedding model**: `BAAI/bge-m3` (multilingual, works well with Chinese text)
- **Chunk schema**: see `scripts/chunk_schema.py`
- **Key design principle**: user data lives outside the skill directory, making backup and migration straightforward.

## Best Practices
- Keep persona files specific and up‑to‑date.
- Write substantive notes; richer content yields better retrieval.
- Periodically re‑index after large note changes.
- Respect privacy – avoid storing highly sensitive data in plain text if the environment is shared.

## Troubleshooting
- **Database errors**: ensure `vector_db/` is writable and dependencies are installed.
- **Poor retrieval**: verify notes contain enough content, try increasing `top_k`, or re‑run the indexing script.
- **Chunking problems**: adjust the logic in `chunk_note_file` or let Claude generate a more sophisticated chunker.
