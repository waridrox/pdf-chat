"""PDF processing service.

Handles text extraction, chunking, and DB persistence for uploaded PDFs.
"""

import fitz  # PyMuPDF
import tiktoken
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.rag_models import Document, Chunk
from app.db.database import AsyncSessionLocal
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# tiktoken encoder for cl100k_base (GPT-3.5 / GPT-4 / text-embedding-3)
_encoder = None


def _get_encoder():
    global _encoder
    if _encoder is None:
        _encoder = tiktoken.get_encoding("cl100k_base")
    return _encoder


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken cl100k_base encoding."""
    return len(_get_encoder().encode(text))


def extract_pages(file_path: str) -> list[str]:
    """Extract text from each page of a PDF using PyMuPDF."""
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return pages


def chunk_text(
    page_texts: list[str],
    max_tokens: int = 800,
    overlap_tokens: int = 100,
) -> list[dict]:
    """Split page texts into chunks of ~max_tokens with overlap.

    Returns list of dicts with keys:
      text, token_count, page_start, page_end
    """
    chunks = []
    encoder = _get_encoder()

    # Build a flat list of (token, page_number) pairs
    all_tokens = []
    for page_idx, page_text in enumerate(page_texts):
        tokens = encoder.encode(page_text)
        for tok in tokens:
            all_tokens.append((tok, page_idx))

    if not all_tokens:
        return chunks

    start = 0
    while start < len(all_tokens):
        end = min(start + max_tokens, len(all_tokens))
        chunk_pairs = all_tokens[start:end]

        token_ids = [p[0] for p in chunk_pairs]
        page_indices = [p[1] for p in chunk_pairs]

        chunk_text_str = encoder.decode(token_ids)
        chunks.append({
            "text": chunk_text_str,
            "token_count": len(token_ids),
            "page_start": min(page_indices),
            "page_end": max(page_indices),
        })

        # Advance by (max_tokens - overlap)
        step = max_tokens - overlap_tokens
        if step <= 0:
            step = max_tokens
        start += step

    return chunks


async def process_document(document_id: int, file_path: str) -> None:
    """Background task: extract text, chunk, and persist to DB."""
    logger.info(f"Processing document {document_id} from {file_path}")

    try:
        # 1. Extract text per page
        page_texts = extract_pages(file_path)
        page_count = len(page_texts)
        logger.info(f"Document {document_id}: extracted {page_count} pages")

        # 2. Chunk the text
        chunks_data = chunk_text(page_texts)
        logger.info(f"Document {document_id}: produced {len(chunks_data)} chunks")

        # 3. Persist to DB
        async with AsyncSessionLocal() as session:
            async with session.begin():
                # Update document with page_count and status
                doc = await session.get(Document, document_id)
                if doc is None:
                    logger.error(f"Document {document_id} not found in DB")
                    return

                doc.page_count = page_count
                doc.metadata_ = {"status": "ready"}

                # Insert chunks
                for idx, chunk_data in enumerate(chunks_data):
                    chunk = Chunk(
                        document_id=document_id,
                        chunk_index=idx,
                        text=chunk_data["text"],
                        token_count=chunk_data["token_count"],
                        page_start=chunk_data["page_start"],
                        page_end=chunk_data["page_end"],
                    )
                    session.add(chunk)

        logger.info(f"Document {document_id}: processing complete, {len(chunks_data)} chunks saved")

    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}")
        # Mark document as failed
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    doc = await session.get(Document, document_id)
                    if doc:
                        doc.metadata_ = {"status": "failed", "error": str(e)}
        except Exception as inner_e:
            logger.error(f"Failed to update error status for document {document_id}: {inner_e}")
