from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"

# Наше тимчасове сховище
books_db = []