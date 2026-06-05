"""
Session management utilities.

Provides context managers and utilities for database sessions.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from .connection import SessionLocal


class SessionManager:
    """
    Database session manager.

    Provides utilities for managing database sessions outside of FastAPI.
    """

    @staticmethod
    @contextmanager
    def get_session() -> Generator[Session, None, None]:
        """
        Get a database session with automatic cleanup.

        Usage:
            with SessionManager.get_session() as session:
                # Use session here
                pass
        """
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def execute_with_session(func, *args, **kwargs):
        """
        Execute a function with a database session.

        Args:
            func: Function that takes session as first argument
            *args: Additional arguments for the function
            **kwargs: Additional keyword arguments for the function
        """
        with SessionManager.get_session() as session:
            return func(session, *args, **kwargs)
