"""PDF processing service.

Handles text extraction, chunking, and DB persistence for uploaded PDFs.
"""

import fitz  # PyMuPDF

from app.db.rag_models import Document, Chunk
from app.db.database import AsyncSessionLocal
from app.services.chunker import split_text_into_chunks
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_pages(file_path: str) -> list[str]:
    """Extract text from each page of a PDF using PyMuPDF."""
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return pages


def chunk_pages(
    page_texts: list[str],
    chunk_size_tokens: int = 800,
    overlap_tokens: int = 100,
) -> list[dict]:
    """Chunk page texts and map chunks back to page ranges.

    Returns list of dicts with keys:
      text, token_count, chunk_index, page_start, page_end
    """
    # Build the full text while tracking page boundaries by character offset
    separator = "\n\n"
    page_char_ranges: list[tuple[int, int]] = []  # (start, end) per page
    parts: list[str] = []
    offset = 0
    for i, pt in enumerate(page_texts):
        if i > 0:
            offset += len(separator)
        start = offset
        parts.append(pt)
        offset += len(pt)
        page_char_ranges.append((start, offset))

    full_text = separator.join(page_texts)

    raw_chunks = split_text_into_chunks(
        full_text,
        chunk_size_tokens=chunk_size_tokens,
        overlap_tokens=overlap_tokens,
    )

    # Map each chunk back to page ranges via character search
    results: list[dict] = []
    search_start = 0
    for rc in raw_chunks:
        chunk_text = rc["chunk_text"]
        # Find where this chunk text appears in full_text
        pos = full_text.find(chunk_text, search_start)
        if pos == -1:
            pos = full_text.find(chunk_text)
        if pos == -1:
            # Fallback: can't map, use all pages
            page_start = 0
            page_end = len(page_texts) - 1
        else:
            chunk_end = pos + len(chunk_text)
            page_start = 0
            page_end = len(page_texts) - 1
            for pi, (ps, pe) in enumerate(page_char_ranges):
                if ps <= pos < pe:
                    page_start = pi
                    break
            for pi, (ps, pe) in enumerate(page_char_ranges):
                if ps < chunk_end <= pe:
                    page_end = pi
                    break
            search_start = pos + 1

        results.append({
            "text": chunk_text,
            "token_count": rc["token_count"],
            "chunk_index": rc["chunk_index"],
            "page_start": page_start,
            "page_end": page_end,
        })

    return results


async def process_document(document_id: int, file_path: str) -> None:
    """Background task: extract text, chunk, and persist to DB."""
    logger.info(f"Processing document {document_id} from {file_path}")

    try:
        # 1. Extract text per page
        page_texts = extract_pages(file_path)
        page_count = len(page_texts)
        logger.info(f"Document {document_id}: extracted {page_count} pages")

        # 2. Chunk the text
        chunks_data = chunk_pages(page_texts)
        logger.info(f"Document {document_id}: produced {len(chunks_data)} chunks")

        # 3. Persist chunks to DB and retrieve their IDs
        chunks_inserted = []
        async with AsyncSessionLocal() as session:
            async with session.begin():
                # Update document with page_count
                doc = await session.get(Document, document_id)
                if doc is None:
                    logger.error(f"Document {document_id} not found in DB")
                    return

                doc.page_count = page_count
                # Keep status as processing for now
                doc.metadata_ = {"status": "processing"}

                # Insert chunks
                for chunk_data in chunks_data:
                    chunk = Chunk(
                        document_id=document_id,
                        chunk_index=chunk_data["chunk_index"],
                        text=chunk_data["text"],
                        token_count=chunk_data["token_count"],
                        page_start=chunk_data["page_start"],
                        page_end=chunk_data["page_end"],
                    )
                    session.add(chunk)
                    chunks_inserted.append(chunk)
                
                await session.flush()
                chunks_for_embedding = [{"chunk_id": c.id, "chunk_text": c.text} for c in chunks_inserted]

        logger.info(f"Document {document_id}: processing complete, {len(chunks_data)} chunks saved")

        # 4. Generate embeddings
        logger.info(f"Document {document_id}: generating embeddings...")
        from app.services.embedding_service import EmbeddingsService
        embed_svc = EmbeddingsService()
        await embed_svc.embed_and_store_chunks(document_id, chunks_for_embedding)

        # 5. Mark as ready
        async with AsyncSessionLocal() as session:
            async with session.begin():
                doc = await session.get(Document, document_id)
                if doc:
                    doc.metadata_ = {"status": "ready"}
        
        logger.info(f"Document {document_id}: embeddings generated and document is ready")

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
