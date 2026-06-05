"""
Tests for the FastAPI backend.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from common.database import get_session
from common.models.base import BaseTable

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    """Override the database session for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Set up test database."""
    BaseTable.metadata.create_all(bind=engine)
    yield
    BaseTable.metadata.drop_all(bind=engine)


class TestAPI:
    """Test the FastAPI application."""

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data

    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_core_status(self):
        """Test the core status endpoint."""
        response = client.get("/api/core/status")
        assert response.status_code == 200
        data = response.json()
        assert "engine" in data
        assert "processor" in data

    def test_process_data(self):
        """Test data processing endpoint."""
        test_data = {"id": "test-api", "data": "sample"}
        response = client.post("/api/core/process", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-api"
        assert data["status"] == "completed"

    def test_validate_data(self):
        """Test data validation endpoint."""
        test_data = {"id": "test", "data": {"key": "value"}}
        response = client.post("/api/core/validate", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True


class TestUserAPI:
    """Test the user API endpoints."""

    def test_get_users_empty(self, setup_database):
        """Test getting users when none exist."""
        response = client.get("/api/users/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_create_user(self, setup_database):
        """Test creating a user."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "is_active": True,
        }
        response = client.post("/api/users/", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert "id" in data

    def test_get_user_not_found(self, setup_database):
        """Test getting a non-existent user."""
        response = client.get("/api/users/999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"

    def test_create_duplicate_user(self, setup_database):
        """Test creating a user with duplicate email."""
        user_data = {"email": "duplicate@example.com", "name": "First User"}

        # Create first user
        response1 = client.post("/api/users/", json=user_data)
        assert response1.status_code == 200

        # Try to create duplicate
        response2 = client.post("/api/users/", json=user_data)
        assert response2.status_code == 400
        data = response2.json()
        assert data["detail"] == "Email already registered"
