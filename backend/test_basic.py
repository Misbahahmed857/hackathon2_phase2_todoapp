import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily disable database initialization for testing
import main
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


def test_docs_available(client):
    """Test that docs are available"""
    response = client.get("/docs")
    # This might redirect, but shouldn't return 404
    assert response.status_code in [200, 307]  # 200 for docs, 307 for redirect to docs


if __name__ == "__main__":
    pytest.main([__file__])