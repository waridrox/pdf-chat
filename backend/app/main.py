from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logger import setup_logger
from app.routes.health import router as health_router
from app.routes.notes import router as notes_router
from app.db.database import init_db
from app.config import get_settings

settings = get_settings()
logger = setup_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, description=settings.APP_DESCRIPTION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(notes_router, prefix="/api")

logger.info("Application routes configured")


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting application")
    try:
        await init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        raise
