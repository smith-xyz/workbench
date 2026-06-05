"""
User models.

Example models showing both Pydantic (API) and SQLAlchemy (database) patterns.
"""

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, BaseTable


# SQLAlchemy model (database)
class User(BaseTable):
    """User database model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


# Pydantic models (API)
class UserBase(BaseModel):
    """Base user fields."""

    email: str
    name: str
    is_active: bool = True


class UserCreate(UserBase):
    """Model for creating users."""

    pass


class UserUpdate(BaseModel):
    """Model for updating users."""

    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Model for user API responses."""

    id: int
