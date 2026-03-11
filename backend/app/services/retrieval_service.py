"""Retrieval service for pgvector nearest-neighbor chunk search.

Embeds a user query via OpenAI and finds the top-k most similar chunks
using the ``<->`` (L2 distance) operator on the embeddings table.
"""

from __future__ import annotations

import os
from typing import List

import openai
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# SQL for pgvector nearest-neighbor search
_RETRIEVAL_SQL = text("""
    SELECT
        c.id        AS chunk_id,
        c.text      AS chunk_text,
        c.chunk_index,
        c.document_id,
        c.page_start,
        c.page_end,
        c.token_count,
        e.embedding <-> :query_vector AS distance
    FROM embeddings e
    JOIN chunks c ON e.chunk_id = c.id
    ORDER BY distance
    LIMIT :top_k
""")


async def retrieve_relevant_chunks(
    question: str,
    top_k: int = 5,
    model: str = "text-embedding-3-large",
    api_key_env: str = "OPENAI_API_KEY",
) -> List[dict]:
    """Embed *question* and return the *top_k* closest chunks.

    Parameters
    ----------
    question : str
        The user's natural-language query.
    top_k : int
        Number of results to return.
    model : str
        OpenAI embedding model to use (must match the model used at indexing).
    api_key_env : str
        Name of the environment variable holding the OpenAI API key.

    Returns
    -------
    list[dict]
        Each dict contains: ``chunk_id``, ``chunk_text``, ``chunk_index``,
        ``document_id``, ``page_start``, ``page_end``, ``token_count``,
        ``distance``.  Ordered closest-first.
    """
    # 1. Embed the question
    api_key = os.environ.get(api_key_env, "")
    if not api_key:
        raise ValueError(f"Environment variable {api_key_env} is not set.")

    client = openai.AsyncOpenAI(api_key=api_key)
    response = await client.embeddings.create(input=[question], model=model)
    query_vector = response.data[0].embedding

    logger.info(f"Embedded query ({len(query_vector)} dims), retrieving top {top_k}")

    # 2. Query pgvector — pass vector as a string literal '[0.1, 0.2, ...]'
    vector_str = "[" + ",".join(str(v) for v in query_vector) + "]"

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            _RETRIEVAL_SQL,
            {"query_vector": vector_str, "top_k": top_k},
        )
        rows = result.fetchall()

    # 3. Format results
    chunks = []
    for row in rows:
        chunks.append({
            "chunk_id": row.chunk_id,
            "chunk_text": row.chunk_text,
            "chunk_index": row.chunk_index,
            "document_id": row.document_id,
            "page_start": row.page_start,
            "page_end": row.page_end,
            "token_count": row.token_count,
            "distance": float(row.distance),
        })

    logger.info(f"Retrieved {len(chunks)} chunks for query")
    return chunks
