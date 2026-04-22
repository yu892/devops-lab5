import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.mark.asyncio
async def test_get_existed_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/users/1")
        assert response.status_code == 200
        assert response.json() == {"id": 1, "name": "John Doe", "email": "john@example.com"}

@pytest.mark.asyncio
async def test_get_non_existed_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        new_user = {"name": "Alice", "email": "alice@example.com"}
        response = await client.post("/users/", json=new_user)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert "id" in data

@pytest.mark.asyncio
async def test_update_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        updated = {"name": "Jane Doe"}
        response = await client.put("/users/1", json=updated)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"

@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/users/1")
        assert response.status_code == 204
