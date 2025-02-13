from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import Note
from app.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/notes")
async def create_note(title: str, content: str, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating new note with title: {title}")
    try:
        note = Note(title=title, content=content)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        logger.info(f"Successfully created note with id: {note.id}")
        return note
    except Exception as e:
        logger.error(f"Error creating note: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating note")


@router.get("/notes")
async def get_notes(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching all notes")
    try:
        result = await db.execute(select(Note))
        notes = result.scalars().all()
        logger.info(f"Successfully fetched {len(notes)} notes")
        return notes
    except Exception as e:
        logger.error(f"Error fetching notes: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching notes")
