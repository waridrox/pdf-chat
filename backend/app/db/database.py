from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.utils.logger import setup_logger
from app.config import get_settings

settings = get_settings()
logger = setup_logger(__name__)

# Create async engine with proper connection pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False,  # Set to True for SQL query logging
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Dependency for getting database session
async def get_db():
    """
    Dependency that provides a database session.
    Ensures proper handling of connections and error cases.
    """
    session = AsyncSessionLocal()
    logger.debug("Creating new database session")
    try:
        yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        await session.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        await session.close()


# Initialize database tables
async def init_db():
    """Initialize database tables and perform any startup database operations."""
    logger.info("Initializing database")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
