"""Unit tests for the retrieval service.

Mocks OpenAI embedding + DB to verify the retrieval pipeline returns
correct results without needing a real Postgres/pgvector instance.
"""
import pytest
import os
import random
from unittest.mock import AsyncMock, patch, MagicMock
from contextlib import asynccontextmanager

os.environ["OPENAI_API_KEY"] = "test-key"
from app.services.retrieval_service import retrieve_relevant_chunks


def _random_vector(dim: int = 3072) -> list[float]:
    """Small deterministic-ish random vector for testing."""
    return [random.random() for _ in range(dim)]


def _make_fake_rows(n: int = 10):
    """Create n fake DB rows as named-tuple-like objects."""
    rows = []
    for i in range(n):
        row = MagicMock()
        row.chunk_id = i + 1
        row.chunk_text = f"chunk text {i}"
        row.chunk_index = i
        row.document_id = 1
        row.page_start = 0
        row.page_end = 0
        row.token_count = 50
        row.distance = 0.1 * (i + 1)
        rows.append(row)
    return rows


@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_retrieve_returns_top_k(mock_async_openai):
    """Insert 10 synthetic rows, retrieve top 5, verify count and order."""
    # Mock OpenAI embedding response
    mock_client = MagicMock()
    dummy_embedding = MagicMock()
    dummy_embedding.embedding = _random_vector()
    dummy_response = MagicMock()
    dummy_response.data = [dummy_embedding]
    mock_client.embeddings.create = AsyncMock(return_value=dummy_response)
    mock_async_openai.return_value = mock_client

    # Mock DB session
    fake_rows = _make_fake_rows(5)
    mock_result = MagicMock()
    mock_result.fetchall.return_value = fake_rows

    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    @asynccontextmanager
    async def mock_session_local():
        yield mock_session

    with patch("app.services.retrieval_service.AsyncSessionLocal", mock_session_local):
        chunks = await retrieve_relevant_chunks("What is RAG?", top_k=5)

    assert len(chunks) == 5
    assert chunks[0]["chunk_id"] == 1
    assert chunks[0]["distance"] < chunks[-1]["distance"]
    # Verify OpenAI was called with the question
    mock_client.embeddings.create.assert_called_once()
    call_args = mock_client.embeddings.create.call_args
    assert call_args.kwargs["input"] == ["What is RAG?"]


@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_retrieve_empty_result(mock_async_openai):
    """Query returns no rows when embeddings table is empty."""
    mock_client = MagicMock()
    dummy_embedding = MagicMock()
    dummy_embedding.embedding = _random_vector()
    dummy_response = MagicMock()
    dummy_response.data = [dummy_embedding]
    mock_client.embeddings.create = AsyncMock(return_value=dummy_response)
    mock_async_openai.return_value = mock_client

    mock_result = MagicMock()
    mock_result.fetchall.return_value = []
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    @asynccontextmanager
    async def mock_session_local():
        yield mock_session

    with patch("app.services.retrieval_service.AsyncSessionLocal", mock_session_local):
        chunks = await retrieve_relevant_chunks("No results query", top_k=5)

    assert chunks == []
