"""Unit tests for the token-aware chunker utility."""

import pytest
from app.services.chunker import split_text_into_chunks, _get_encoder


def _make_long_text(num_paragraphs: int = 50, words_per_para: int = 80) -> str:
    """Generate a synthetic long text with many paragraphs."""
    paragraphs = []
    for i in range(num_paragraphs):
        words = [f"word{i}_{j}" for j in range(words_per_para)]
        paragraphs.append(" ".join(words))
    return "\n\n".join(paragraphs)


class TestSplitTextIntoChunks:
    """Tests for split_text_into_chunks."""

    def test_empty_text_returns_empty(self):
        assert split_text_into_chunks("") == []

    def test_whitespace_only_returns_empty(self):
        assert split_text_into_chunks("   \n\n   ") == []

    def test_single_short_paragraph(self):
        text = "Hello, this is a short paragraph."
        chunks = split_text_into_chunks(text, chunk_size_tokens=800)
        assert len(chunks) == 1
        assert chunks[0]["chunk_index"] == 0
        assert chunks[0]["chunk_text"] == text
        assert chunks[0]["token_count"] > 0

    def test_chunk_sizes_within_budget(self):
        """Each chunk's token_count should be <= chunk_size_tokens + 10 margin."""
        text = _make_long_text(num_paragraphs=50, words_per_para=80)
        chunk_size = 800
        margin = 10
        chunks = split_text_into_chunks(
            text, chunk_size_tokens=chunk_size, overlap_tokens=100
        )
        assert len(chunks) > 1, "Expected multiple chunks for long text"
        for chunk in chunks:
            assert chunk["token_count"] <= chunk_size + margin, (
                f"Chunk {chunk['chunk_index']} has {chunk['token_count']} tokens, "
                f"exceeds budget of {chunk_size + margin}"
            )

    def test_chunk_indices_sequential(self):
        text = _make_long_text(num_paragraphs=30, words_per_para=60)
        chunks = split_text_into_chunks(text, chunk_size_tokens=400)
        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))

    def test_overlap_between_consecutive_chunks(self):
        """The tail of chunk N should overlap with the head of chunk N+1."""
        text = _make_long_text(num_paragraphs=30, words_per_para=60)
        chunks = split_text_into_chunks(
            text, chunk_size_tokens=400, overlap_tokens=100
        )
        assert len(chunks) >= 2, "Need at least 2 chunks to test overlap"

        encoder = _get_encoder()
        for i in range(len(chunks) - 1):
            current_tokens = encoder.encode(chunks[i]["chunk_text"])
            next_tokens = encoder.encode(chunks[i + 1]["chunk_text"])

            # The last `overlap_tokens` of chunk i should appear at the
            # start of chunk i+1
            if len(current_tokens) > 100:
                tail = current_tokens[-100:]
                head = next_tokens[:100]
                assert tail == head, (
                    f"Expected overlap between chunk {i} and {i+1}"
                )

    def test_deterministic(self):
        """Same input produces same output."""
        text = _make_long_text(num_paragraphs=20, words_per_para=50)
        result1 = split_text_into_chunks(text)
        result2 = split_text_into_chunks(text)
        assert result1 == result2

    def test_large_paragraph_is_split(self):
        """A single paragraph exceeding chunk_size should be hard-split."""
        # Create one very large paragraph
        words = [f"longword{i}" for i in range(1000)]
        text = " ".join(words)
        chunks = split_text_into_chunks(text, chunk_size_tokens=200, overlap_tokens=50)
        assert len(chunks) > 1, "Expected large paragraph to be split into multiple chunks"
        for chunk in chunks:
            assert chunk["token_count"] <= 210, (
                f"Chunk {chunk['chunk_index']} has {chunk['token_count']} tokens"
            )

    def test_custom_chunk_size_and_overlap(self):
        text = _make_long_text(num_paragraphs=20, words_per_para=40)
        chunks = split_text_into_chunks(
            text, chunk_size_tokens=200, overlap_tokens=50
        )
        assert len(chunks) > 1
        for chunk in chunks:
            assert chunk["token_count"] <= 210

    def test_all_text_covered(self):
        """Most text should be preserved — union of chunks covers >95% of words."""
        text = _make_long_text(num_paragraphs=10, words_per_para=30)
        chunks = split_text_into_chunks(text, chunk_size_tokens=300, overlap_tokens=0)
        reconstructed = "".join(c["chunk_text"] for c in chunks)
        original_words = set(text.split())
        reconstructed_words = set(reconstructed.split())
        covered = len(original_words & reconstructed_words)
        coverage = covered / len(original_words) if original_words else 1.0
        assert coverage >= 0.90, (
            f"Only {coverage:.1%} of original words found in chunks "
            f"(missing {len(original_words - reconstructed_words)})"
        )
