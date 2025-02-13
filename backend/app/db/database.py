from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.utils.logger import setup_logger
from app.config import get_settings

settings = get_settings()
logger = setup_logger(__name__)

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Dependency for getting database session
async def get_db():
    logger.debug("Creating new database session")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            logger.debug("Database session closed successfully")
        except Exception as e:
            logger.error(f"Error in database session: {str(e)}")
            raise
        finally:
            await session.close()


# Initialize database tables
async def init_db():
    logger.info("Initializing database")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
