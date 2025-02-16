import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    APP_NAME: str = "FastAPI React Starter"
    APP_DESCRIPTION: str = "FastAPI React Starter Template"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

BASE_DIR = Path(__file__).parent.parent

# Logging configuration
LOGGING_CONFIG = {
    "development": {
        "log_level": "DEBUG",
        "log_dir": BASE_DIR / "logs" / "dev",
    },
    "production": {
        "log_level": "INFO",
        "log_dir": BASE_DIR / "logs" / "prod",
    },
    "testing": {
        "log_level": "DEBUG",
        "log_dir": None,  # Console only
    },
}

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
CURRENT_LOGGING_CONFIG = LOGGING_CONFIG[ENVIRONMENT]
