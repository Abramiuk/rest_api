from uuid import UUID
from models import books_db

class BookRepository:
    async def get_all(self):
        return books_db

    async def get_by_id(self, book_id: UUID):
        for book in books_db:
            if book["id"] == book_id:
                return book
        return None

    async def add(self, book_data: dict):
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: UUID):
        for i, book in enumerate(books_db):
            if book["id"] == book_id:
                del books_db[i]
                return True
        return False