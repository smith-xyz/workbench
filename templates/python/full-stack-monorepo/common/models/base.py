"""
Base models for the application.

Contains base Pydantic and SQLAlchemy models.
"""

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(PydanticBaseModel):
    """
    Base Pydantic model with common configuration.
    """

    model_config = {
        "from_attributes": True,
        "validate_assignment": True,
        "arbitrary_types_allowed": True,
    }


class BaseTable(DeclarativeBase):
    """
    Base SQLAlchemy model with common fields.

    Provides created_at and updated_at timestamps for all tables.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
