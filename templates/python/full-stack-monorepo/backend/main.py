"""
FastAPI application entry point.

Main application setup and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.database.connection import create_tables

from .routes import api_router

# Create FastAPI app
app = FastAPI(
    title="Project Template API",
    description="A full-stack Python application template",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize the application."""
    # Create database tables
    create_tables()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Project Template API",
        "docs": "/api/docs",
        "redoc": "/api/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
