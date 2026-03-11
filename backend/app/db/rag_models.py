"""RAG-related SQLAlchemy ORM models.

Tables: documents, chunks, embeddings, chat_sessions, chat_messages.
"""

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Text,
    String,
    DateTime,
    ForeignKey,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(Text, nullable=False)
    uploaded_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    page_count = Column(Integer, nullable=True)
    file_size_bytes = Column(BigInteger, nullable=True)
    metadata_ = Column("metadata", JSONB, server_default=text("'{}'::jsonb"))

    # Relationships
    chunks = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan"
    )
    chat_sessions = relationship(
        "ChatSession", back_populates="document"
    )

    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}')>"


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=True)
    page_start = Column(Integer, nullable=True)
    page_end = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    document = relationship("Document", back_populates="chunks")
    embeddings = relationship(
        "Embedding", back_populates="chunk", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Chunk(id={self.id}, document_id={self.document_id}, "
            f"chunk_index={self.chunk_index})>"
        )


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_id = Column(
        Integer,
        ForeignKey("chunks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    embedding = Column(Vector(3072), nullable=False)
    model = Column(String(100), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    chunk = relationship("Chunk", back_populates="embeddings")

    def __repr__(self):
        return f"<Embedding(id={self.id}, chunk_id={self.chunk_id}, model='{self.model}')>"


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    started_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    document = relationship("Document", back_populates="chat_sessions")
    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ChatSession(id={self.id}, document_id={self.document_id})>"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    session = relationship("ChatSession", back_populates="messages")

    def __repr__(self):
        return (
            f"<ChatMessage(id={self.id}, session_id={self.session_id}, "
            f"role='{self.role}')>"
        )
