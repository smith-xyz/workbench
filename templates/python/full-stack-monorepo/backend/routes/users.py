"""
User API routes.

Example CRUD routes for user management.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common.database import get_session
from common.models.user import User, UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """Get all users."""
    users = session.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a specific user."""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """Create a new user."""
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user = User(**user_data.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)
):
    """Update a user."""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user."""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
