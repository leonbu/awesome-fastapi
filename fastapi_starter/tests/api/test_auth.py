import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register user
    register_payload = {
        "email": "tester@example.com",
        "password": "secretpassword123",
        "full_name": "FastAPI Tester",
    }
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "tester@example.com"
    assert "id" in data
    assert "hashed_password" not in data

    # Login with credentials
    login_data = {
        "username": "tester@example.com",
        "password": "secretpassword123",
    }
    login_resp = await client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == 200
    token_json = login_resp.json()
    assert "access_token" in token_json
    assert token_json["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    login_resp = await client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_resp.status_code == 401
