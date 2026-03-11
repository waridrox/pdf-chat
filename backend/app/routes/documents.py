"""Document upload and management routes."""

import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.rag_models import Document
from app.services.pdf_processing import process_document
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "storage", "uploads")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_MIME_TYPES = {"application/pdf"}


@router.post("/upload", status_code=201)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload a PDF document for processing.

    Validates the file, saves it to disk, creates a DB entry,
    and enqueues a background task for text extraction and chunking.
    """
    # Validate mime type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {file.content_type}. Only PDF files are accepted.",
        )

    # Read file content and validate size
    content = await file.read()
    file_size = len(content)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({file_size} bytes). Maximum allowed: {MAX_FILE_SIZE} bytes (100 MB).",
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file
    file_uuid = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_uuid}.pdf")

    with open(file_path, "wb") as f:
        f.write(content)

    logger.info(f"Saved upload to {file_path} ({file_size} bytes)")

    # Create DB entry
    doc = Document(
        filename=file.filename or "untitled.pdf",
        file_size_bytes=file_size,
        metadata_={"status": "processing"},
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    logger.info(f"Created document record id={doc.id}")

    # Enqueue background processing
    background_tasks.add_task(process_document, doc.id, file_path)

    return {"document_id": doc.id, "status": "processing"}
