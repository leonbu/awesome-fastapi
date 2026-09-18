import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user_me(client: AsyncClient):
    # Register
    await client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "password123", "full_name": "Alice"},
    )

    # Login
    login_res = await client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_res.json()["access_token"]

    # Profile check
    me_res = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    profile = me_res.json()
    assert profile["email"] == "alice@example.com"
    assert profile["full_name"] == "Alice"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
