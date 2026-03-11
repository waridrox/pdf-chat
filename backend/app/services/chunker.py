"""Token-aware text chunker for RAG pipelines.

Splits text into chunks by aggregating paragraphs until a token budget
is reached, then carries overlap tokens into the next chunk.
Deterministic and idempotent for the same input.
"""

from __future__ import annotations

from typing import Any, List

import tiktoken

# Lazy-loaded singleton encoder
_encoder: tiktoken.Encoding | None = None


def _get_encoder() -> tiktoken.Encoding:
    global _encoder
    if _encoder is None:
        _encoder = tiktoken.get_encoding("cl100k_base")
    return _encoder


def _count_tokens(text: str, tokenizer: Any = None) -> int:
    """Count tokens in *text* using the provided tokenizer or the default."""
    if tokenizer is not None:
        return len(tokenizer.encode(text))
    return len(_get_encoder().encode(text))


def _encode(text: str, tokenizer: Any = None) -> list[int]:
    if tokenizer is not None:
        return tokenizer.encode(text)
    return _get_encoder().encode(text)


def _decode(token_ids: list[int], tokenizer: Any = None) -> str:
    if tokenizer is not None:
        return tokenizer.decode(token_ids)
    return _get_encoder().decode(token_ids)


def split_text_into_chunks(
    text: str,
    tokenizer: Any = None,
    chunk_size_tokens: int = 800,
    overlap_tokens: int = 100,
) -> List[dict]:
    """Split *text* into token-bounded chunks with overlap.

    Strategy
    --------
    1. Split by paragraphs (double newlines).
    2. Aggregate paragraphs until near *chunk_size_tokens*.
    3. If a single paragraph exceeds the budget, hard-split at token boundaries.
    4. Carry the last *overlap_tokens* worth of text into the next chunk.

    Returns
    -------
    List of dicts: ``{"chunk_text": str, "token_count": int, "chunk_index": int}``
    """
    if not text or not text.strip():
        return []

    paragraphs = text.split("\n\n")
    # Remove empty paragraphs but preserve whitespace within paragraphs
    paragraphs = [p for p in paragraphs if p.strip()]

    if not paragraphs:
        return []

    chunks: List[dict] = []
    current_tokens: list[int] = []
    chunk_index = 0

    for para in paragraphs:
        para_tokens = _encode(para, tokenizer)

        # If a single paragraph exceeds the budget, hard-split it
        if len(para_tokens) > chunk_size_tokens:
            # Flush current buffer first if non-empty
            if current_tokens:
                chunks.append({
                    "chunk_text": _decode(current_tokens, tokenizer),
                    "token_count": len(current_tokens),
                    "chunk_index": chunk_index,
                })
                chunk_index += 1
                # Carry overlap
                if overlap_tokens > 0 and len(current_tokens) > overlap_tokens:
                    current_tokens = current_tokens[-overlap_tokens:]
                else:
                    current_tokens = []

            # Hard-split the large paragraph
            offset = 0
            while offset < len(para_tokens):
                # How much room do we have?
                remaining = chunk_size_tokens - len(current_tokens)
                slice_end = offset + remaining
                current_tokens.extend(para_tokens[offset:slice_end])
                offset = slice_end

                if len(current_tokens) >= chunk_size_tokens:
                    chunks.append({
                        "chunk_text": _decode(current_tokens, tokenizer),
                        "token_count": len(current_tokens),
                        "chunk_index": chunk_index,
                    })
                    chunk_index += 1
                    if overlap_tokens > 0 and len(current_tokens) > overlap_tokens:
                        current_tokens = current_tokens[-overlap_tokens:]
                    else:
                        current_tokens = []
            continue

        # Normal case: paragraph fits within budget
        if len(current_tokens) + len(para_tokens) > chunk_size_tokens:
            # Flush current chunk
            if current_tokens:
                chunks.append({
                    "chunk_text": _decode(current_tokens, tokenizer),
                    "token_count": len(current_tokens),
                    "chunk_index": chunk_index,
                })
                chunk_index += 1
                # Carry overlap
                if overlap_tokens > 0 and len(current_tokens) > overlap_tokens:
                    current_tokens = current_tokens[-overlap_tokens:]
                else:
                    current_tokens = []

        current_tokens.extend(para_tokens)

    # Flush remaining tokens
    if current_tokens:
        chunks.append({
            "chunk_text": _decode(current_tokens, tokenizer),
            "token_count": len(current_tokens),
            "chunk_index": chunk_index,
        })

    return chunks
