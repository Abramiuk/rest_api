from repository import BookRepository
from uuid import uuid4

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(self, status=None, author=None, sort_by=None):
        books = await self.repo.get_all()
        
        # Фільтрація
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]
            
        # Сортування
        if sort_by in ["title", "year"]:
            books = sorted(books, key=lambda x: x[sort_by])
            
        return books

    async def create_book(self, book_data):
        new_book = book_data.model_dump()
        new_book["id"] = uuid4()
        return await self.repo.add(new_book)

    async def get_book_by_id(self, book_id):
        return await self.repo.get_by_id(book_id)

    async def delete_book(self, book_id):
        return await self.repo.delete(book_id)