"""
API routes for the application.
"""

from fastapi import APIRouter

from .core import router as core_router
from .users import router as users_router

# Main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(core_router, prefix="/core", tags=["core"])

__all__ = ["api_router"]
