"""
Tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient
from app import app
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_register_user():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        user_data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "job_seeker"
        }

        response = await client.post("/api/auth/register", json=user_data)
        assert response.status_code in [200, 201]  # Success or already exists

        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data
            assert "user_id" in data
            assert data["role"] == "job_seeker"

@pytest.mark.asyncio
async def test_login_user():
    """Test user login"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }

        response = await client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_login():
    """Test invalid login credentials"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        login_data = {
            "username": "nonexistent",
            "password": "wrongpass"
        }

        response = await client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without authentication"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/api/users/profile")
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
