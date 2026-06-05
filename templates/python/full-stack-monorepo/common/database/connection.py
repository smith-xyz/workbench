"""
Database connection management.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from common.models.base import BaseTable

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create engine
engine = create_engine(
    DATABASE_URL, echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database_url() -> str:
    """Get the database URL."""
    return DATABASE_URL


def create_tables():
    """Create all database tables."""
    BaseTable.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    For use with FastAPI dependency injection.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
