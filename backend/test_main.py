import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app from main.py in the same directory
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


def test_read_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo Web Application API is running!"}


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "todo-api"}


def test_auth_routes_exist(client):
    """Test that auth routes are accessible (even if they return 422 for missing data)"""
    # Test that the route exists (will return 422 for missing data, not 404)
    response = client.post("/auth/register")
    assert response.status_code in [422, 400]  # Unprocessable Entity or Bad Request for missing data

    response = client.post("/auth/login")
    assert response.status_code in [422, 400]  # Unprocessable Entity or Bad Request for missing data


def test_todos_routes_exist(client):
    """Test that todos routes are accessible (should return 401 without auth)"""
    # These routes should require authentication, so expect 401
    response = client.get("/todos/")
    assert response.status_code == 401  # Unauthorized

    response = client.post("/todos/")
    assert response.status_code == 401  # Unauthorized


if __name__ == "__main__":
    pytest.main([__file__])