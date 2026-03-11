"""Embedding service for generating and storing OpenAI vector embeddings.

Batches chunk texts, calls the OpenAI embeddings API with retry logic,
and persists vectors to the embeddings table.
"""

from __future__ import annotations

import asyncio
import os
import logging
from typing import List

import openai
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.rag_models import Embedding, Chunk
from app.db.database import AsyncSessionLocal
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingsService:
    """Generates and stores embeddings for document chunks."""

    def __init__(
        self,
        api_key_env: str = "OPENAI_API_KEY",
        model: str = "text-embedding-3-large",
        batch_size: int = 50,
        max_retries: int = 3,
    ):
        api_key = os.environ.get(api_key_env, "")
        if not api_key:
            raise ValueError(
                f"Environment variable {api_key_env} is not set. "
                "Please provide a valid OpenAI API key."
            )
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
        self.batch_size = batch_size
        self.max_retries = max_retries

    async def _embed_batch_with_retry(
        self, texts: List[str]
    ) -> List[List[float]]:
        """Call OpenAI embeddings API with exponential backoff on 429."""
        for attempt in range(self.max_retries):
            try:
                response = await self.client.embeddings.create(
                    input=texts,
                    model=self.model,
                )
                return [item.embedding for item in response.data]

            except openai.RateLimitError as e:
                if attempt == self.max_retries - 1:
                    logger.error(
                        f"Rate limit exceeded after {self.max_retries} retries"
                    )
                    raise
                wait = 2 ** (attempt + 1)  # 2s, 4s, 8s
                logger.warning(
                    f"Rate limited (429), retrying in {wait}s "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )
                await asyncio.sleep(wait)

            except openai.APIError as e:
                if attempt == self.max_retries - 1:
                    raise
                wait = 2 ** (attempt + 1)
                logger.warning(
                    f"API error: {e}, retrying in {wait}s "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )
                await asyncio.sleep(wait)

        # Should never reach here, but just in case
        raise RuntimeError("Exhausted retries without success or exception")

    async def embed_and_store_chunks(
        self,
        document_id: int,
        chunks: List[dict],
    ) -> int:
        """Generate embeddings for chunks and store in DB.

        Parameters
        ----------
        document_id : int
            The document these chunks belong to.
        chunks : list[dict]
            Each dict must have keys: ``chunk_id`` (int) and ``chunk_text`` (str).

        Returns
        -------
        int
            Number of embeddings stored.
        """
        total_stored = 0

        for batch_start in range(0, len(chunks), self.batch_size):
            batch = chunks[batch_start : batch_start + self.batch_size]
            texts = [c["chunk_text"] for c in batch]
            chunk_ids = [c["chunk_id"] for c in batch]

            logger.info(
                f"Document {document_id}: embedding batch "
                f"{batch_start // self.batch_size + 1} "
                f"({len(batch)} chunks)"
            )

            vectors = await self._embed_batch_with_retry(texts)

            # Store in DB — one transaction per batch to avoid long locks
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    for chunk_id, vector in zip(chunk_ids, vectors):
                        emb = Embedding(
                            chunk_id=chunk_id,
                            embedding=vector,
                            model=self.model,
                        )
                        session.add(emb)

            total_stored += len(vectors)
            logger.info(
                f"Document {document_id}: stored {len(vectors)} embeddings "
                f"(batch {batch_start // self.batch_size + 1})"
            )

        logger.info(
            f"Document {document_id}: embedding complete, "
            f"{total_stored} total embeddings stored"
        )
        return total_stored
