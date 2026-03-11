"""Unit tests for the embedding service.

Mocks the OpenAI API to verify batching, retries, and database inserts.
"""
import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from contextlib import asynccontextmanager

# Set API key before importing so init doesn't fail
os.environ["OPENAI_API_KEY"] = "test-key"
import openai
from app.services.embedding_service import EmbeddingsService


class DummyItem:
    def __init__(self, emb):
        self.embedding = emb


class DummyResponse:
    def __init__(self, count=10):
        self.data = [DummyItem([0.1] * 1536) for _ in range(count)]


def _make_mock_session():
    """Create a properly mocked async session with begin() context manager."""
    mock_session = MagicMock()
    mock_session.add = MagicMock()

    # Mock session.begin() as an async context manager
    @asynccontextmanager
    async def mock_begin():
        yield

    mock_session.begin = mock_begin
    return mock_session


def _make_mock_session_local(mock_session):
    """Create a mock for AsyncSessionLocal that works as `async with`."""
    @asynccontextmanager
    async def mock_session_local():
        yield mock_session

    return mock_session_local


@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_embed_and_store_chunks_success(mock_async_openai):
    """10 chunks → 10 DB inserts, 1 API call."""
    # Setup OpenAI mock
    mock_client = MagicMock()
    mock_client.embeddings.create = AsyncMock(return_value=DummyResponse(10))
    mock_async_openai.return_value = mock_client

    # Setup DB mock
    mock_session = _make_mock_session()
    mock_session_local = _make_mock_session_local(mock_session)

    with patch("app.services.embedding_service.AsyncSessionLocal", mock_session_local):
        service = EmbeddingsService()
        chunks = [{"chunk_id": i, "chunk_text": f"text {i}"} for i in range(10)]
        stored = await service.embed_and_store_chunks(document_id=1, chunks=chunks)

    assert stored == 10
    assert mock_client.embeddings.create.call_count == 1
    assert mock_session.add.call_count == 10


@pytest.mark.asyncio
@patch("openai.AsyncOpenAI")
async def test_retry_on_429_rate_limit(mock_async_openai):
    """429 on first call → retry → success on second call."""
    mock_client = MagicMock()
    rate_limit_err = openai.RateLimitError(
        message="Rate limit", response=MagicMock(status_code=429), body={}
    )
    mock_client.embeddings.create = AsyncMock(
        side_effect=[rate_limit_err, DummyResponse(10)]
    )
    mock_async_openai.return_value = mock_client

    mock_session = _make_mock_session()
    mock_session_local = _make_mock_session_local(mock_session)

    with patch("app.services.embedding_service.AsyncSessionLocal", mock_session_local):
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            service = EmbeddingsService()
            chunks = [{"chunk_id": i, "chunk_text": f"text {i}"} for i in range(10)]
            stored = await service.embed_and_store_chunks(document_id=2, chunks=chunks)

    assert stored == 10
    assert mock_client.embeddings.create.call_count == 2
    mock_sleep.assert_called_once_with(2)  # 2^(0+1) = 2s on first retry
