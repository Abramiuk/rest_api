from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import Optional
from models import BookStatus

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    year: int = Field(..., gt=0)
    status: BookStatus = BookStatus.AVAILABLE

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: UUID = Field(default_factory=uuid4)

class BookResponse(Book):
    model_config = ConfigDict(from_attributes=True) 