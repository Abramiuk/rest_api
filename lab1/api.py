from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID
from typing import List, Optional

# Імпортуємо наші модулі
from schemas import BookCreate, BookResponse
from services import BookService
from models import BookStatus

# Створюємо роутер
router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_all_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    # Використовуємо pattern замість regex для сумісності з FastAPI 0.100+
    sort_by: Optional[str] = Query(None, pattern="^(title|year)$")
):
    """Отримання списку всіх книг з фільтрацією та сортуванням"""
    return await service.get_books(status, author, sort_by)

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID):
    """Отримання конкретної книги по ID"""
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """Додавання нової книги"""
    return await service.create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    """
    Видалення книги (Ідемпотентне). 
    Завжди повертає 204, навіть якщо книги вже не існує.
    """
    await service.delete_book(book_id)
    # У DELETE 204 ми не повертаємо тіло відповіді
    return None