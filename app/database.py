import os
from typing import Any, Dict

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

PLACEHOLDER_MARKERS = {"usuario:contraseña", "@host", "opunnence_db"}
DEFAULT_SQLITE_URL = "sqlite:///./opunnence.db"


def _normalize_database_url(raw_url: str) -> str:
    """Ensure PostgreSQL URLs use the psycopg driver for SQLAlchemy."""
    if raw_url.startswith("postgresql://") and "+psycopg" not in raw_url:
        return raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return raw_url


def _resolve_database_config() -> tuple[str, Dict[str, Any]]:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url or any(marker in database_url for marker in PLACEHOLDER_MARKERS):
        # Fallback to local SQLite for development when no valid DATABASE_URL is provided.
        return DEFAULT_SQLITE_URL, {"check_same_thread": False}
    return _normalize_database_url(database_url), {}


DATABASE_URL, CONNECT_ARGS = _resolve_database_config()
engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
