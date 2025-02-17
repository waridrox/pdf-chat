from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.utils.logger import setup_logger
from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.db.database import init_db, engine
from app.config import get_settings

settings = get_settings()
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting application")
    try:
        await init_db()
        logger.info("Application started successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Cleanup
        logger.info("Shutting down application")
        await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
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
app.include_router(auth_router, prefix="/api")

logger.info("Application routes configured")
