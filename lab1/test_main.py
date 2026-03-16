import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_and_get_book():
    transport = ASGITransport(app=app)
    # Змінюємо base_url на більш стандартний для тестів
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        # 1. Створення
        payload = {
            "title": "Kobzar", 
            "author": "Shevchenko", 
            "year": 1840,
            "status": "available"
        }
        response = await ac.post("/books/", json=payload)
        assert response.status_code == 201
        data = response.json()
        book_id = data["id"]

        # 2. Отримання по ID
        # Важливо: переконайся, що тут немає зайвих слейшів
        response = await ac.get(f"/books/{book_id}")
        
        # Якщо знову буде 405, цей принт допоможе зрозуміти, куди саме йде запит
        if response.status_code == 405:
            print(f"\nDebug: Requested URL: {response.url}")
            print(f"Debug: Response headers: {response.headers}")

        assert response.status_code == 200
        assert response.json()["title"] == "Kobzar"

@pytest.mark.asyncio
async def test_delete_idempotency():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        # Використовуємо валідний UUID
        test_id = "550e8400-e29b-41d4-a716-446655440000"
        
        response = await ac.delete(f"/books/{test_id}")
        assert response.status_code == 204
        
        response = await ac.delete(f"/books/{test_id}")
        assert response.status_code == 204