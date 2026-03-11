"""Add RAG schema (documents, chunks, embeddings, chat_sessions, chat_messages)

Revision ID: a1b2c3d4e5f6
Revises: e33bb845793c
Create Date: 2026-03-11 15:50:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "e33bb845793c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # --- documents ---
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("filename", sa.Text, nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True)),
        sa.Column("page_count", sa.Integer, nullable=True),
        sa.Column("file_size_bytes", sa.BigInteger, nullable=True),
        sa.Column("metadata", JSONB),
    )
    op.execute("ALTER TABLE documents ALTER COLUMN uploaded_at SET DEFAULT now();")
    op.execute("ALTER TABLE documents ALTER COLUMN metadata SET DEFAULT '{}'::jsonb;")

    # --- chunks ---
    op.create_table(
        "chunks",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "document_id",
            sa.Integer,
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("chunk_index", sa.Integer, nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("token_count", sa.Integer, nullable=True),
        sa.Column("page_start", sa.Integer, nullable=True),
        sa.Column("page_end", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute("ALTER TABLE chunks ALTER COLUMN created_at SET DEFAULT now();")
    op.create_index(
        "ix_chunks_document_id", "chunks", ["document_id"]
    )

    # --- embeddings ---
    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "chunk_id",
            sa.Integer,
            sa.ForeignKey("chunks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("model", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute("ALTER TABLE embeddings ALTER COLUMN created_at SET DEFAULT now();")
    # Add vector column via raw SQL (Alembic has no built-in vector type)
    op.execute(
        "ALTER TABLE embeddings ADD COLUMN embedding vector(3072) NOT NULL;"
    )
    op.create_index(
        "ix_embeddings_chunk_id", "embeddings", ["chunk_id"]
    )

    # --- chat_sessions ---
    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "document_id",
            sa.Integer,
            sa.ForeignKey("documents.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
        ),
    )
    op.execute("ALTER TABLE chat_sessions ALTER COLUMN started_at SET DEFAULT now();")

    # --- chat_messages ---
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "session_id",
            sa.Integer,
            sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute("ALTER TABLE chat_messages ALTER COLUMN created_at SET DEFAULT now();")
    op.create_index(
        "ix_chat_messages_session_id", "chat_messages", ["session_id"]
    )


def downgrade() -> None:
    op.drop_table("chat_messages")
    op.drop_table("chat_sessions")
    op.drop_table("embeddings")
    op.drop_table("chunks")
    op.drop_table("documents")
    op.execute("DROP EXTENSION IF EXISTS vector;")
