import pytest
import httpx
from main import app

@pytest.mark.asyncio
async def test_create_book():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/books/", json={
            "title": "Kobzar",
            "author": "Taras Shevchenko",
            "year": 1840,
            "status": "Available in library"
        })
    assert response.status_code == 201
    assert response.json()["title"] == "Kobzar"

@pytest.mark.asyncio
async def test_get_all_books():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_book_idempotent():
    import uuid
    fake_id = str(uuid.uuid4())
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.delete(f"/books/{fake_id}")
    assert response.status_code == 204