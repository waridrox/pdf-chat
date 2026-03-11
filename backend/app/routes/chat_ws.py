"""WebSocket chat endpoint with streaming OpenAI responses.

Protocol:
  1. Client connects to /ws/chat
  2. Client sends JSON: {"document_id": X, "question": "..."}
  3. Server retrieves relevant chunks, calls OpenAI chat with stream=True
  4. Server sends {"type": "token", "delta": "..."} per streamed delta
  5. Server sends {"type": "done", "answer": "full text", "sources": [...]} at end
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from collections import deque
from typing import List

import openai
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import text

from app.db.database import AsyncSessionLocal
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

# Rate-limit settings
RATE_LIMIT_MAX = 10      # max messages
RATE_LIMIT_WINDOW = 60   # per N seconds

# Retrieval SQL (pgvector nearest-neighbor)
_RETRIEVAL_SQL = text("""
    SELECT
        c.id        AS chunk_id,
        c.text      AS chunk_text,
        c.page_start,
        c.page_end,
        e.embedding <-> :query_vector AS distance
    FROM embeddings e
    JOIN chunks c ON e.chunk_id = c.id
    WHERE c.document_id = :document_id
    ORDER BY distance
    LIMIT :top_k
""")


def _build_system_prompt(chunks: List[dict]) -> str:
    """Assemble a system prompt with retrieved context."""
    context = "\n\n---\n\n".join(
        f"[Page {c['page_start']}-{c['page_end']}]\n{c['chunk_text']}"
        for c in chunks
    )
    return (
        "You are a helpful assistant that answers questions based on the "
        "provided document context. Use ONLY the context below to answer. "
        "If the answer is not in the context, say so.\n\n"
        f"## Document Context\n\n{context}"
    )


async def _retrieve_chunks(
    document_id: int, query_vector: List[float], top_k: int = 5
) -> List[dict]:
    """Query pgvector for nearest chunks scoped to a document."""
    vector_str = "[" + ",".join(str(v) for v in query_vector) + "]"
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            _RETRIEVAL_SQL,
            {"query_vector": vector_str, "top_k": top_k, "document_id": document_id},
        )
        rows = result.fetchall()
    return [
        {
            "chunk_id": r.chunk_id,
            "chunk_text": r.chunk_text,
            "page_start": r.page_start,
            "page_end": r.page_end,
            "distance": float(r.distance),
        }
        for r in rows
    ]


@router.websocket("/ws/chat")
async def chat_websocket(ws: WebSocket):
    await ws.accept()
    logger.info("WebSocket client connected")

    # Per-connection rate limiter
    timestamps: deque = deque()

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        await ws.send_json({"type": "error", "message": "OPENAI_API_KEY not configured"})
        await ws.close()
        return

    client = openai.AsyncOpenAI(api_key=api_key)

    try:
        while True:
            raw = await ws.receive_text()

            # Parse message
            try:
                msg = json.loads(raw)
                document_id = int(msg["document_id"])
                question = str(msg["question"]).strip()
                if not question:
                    await ws.send_json({"type": "error", "message": "question is empty"})
                    continue
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                await ws.send_json({"type": "error", "message": f"Invalid message: {e}"})
                continue

            # Rate limit check
            now = time.monotonic()
            while timestamps and timestamps[0] < now - RATE_LIMIT_WINDOW:
                timestamps.popleft()
            if len(timestamps) >= RATE_LIMIT_MAX:
                await ws.send_json({"type": "error", "message": "rate limit"})
                continue
            timestamps.append(now)

            # 1. Embed the question
            try:
                embed_resp = await client.embeddings.create(
                    input=[question], model="text-embedding-3-large"
                )
                query_vector = embed_resp.data[0].embedding
            except Exception as e:
                await ws.send_json({"type": "error", "message": f"Embedding failed: {e}"})
                continue

            # 2. Retrieve relevant chunks
            try:
                chunks = await _retrieve_chunks(document_id, query_vector)
            except Exception as e:
                await ws.send_json({"type": "error", "message": f"Retrieval failed: {e}"})
                continue

            if not chunks:
                await ws.send_json({
                    "type": "error",
                    "message": "No indexed chunks found for this document. Please ensure it has been processed and embedded.",
                })
                continue

            # 3. Build messages for OpenAI
            system_prompt = _build_system_prompt(chunks)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ]

            # 4. Stream the response
            full_answer = ""
            try:
                stream = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    stream=True,
                )
                async for chunk in stream:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        full_answer += delta.content
                        await ws.send_json({"type": "token", "delta": delta.content})
            except WebSocketDisconnect:
                logger.info("Client disconnected during streaming")
                return
            except Exception as e:
                await ws.send_json({"type": "error", "message": f"LLM error: {e}"})
                continue

            # 5. Send done message with sources
            sources = [
                {"page_start": c["page_start"], "page_end": c["page_end"]}
                for c in chunks
            ]
            await ws.send_json({
                "type": "done",
                "answer": full_answer,
                "sources": sources,
            })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await ws.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
