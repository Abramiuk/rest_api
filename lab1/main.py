from fastapi import FastAPI
from api import router

# Створюємо екземпляр застосунку
app = FastAPI(
    title="Library Management API",
    description="API для керування книгами в бібліотеці (Ivan's Project)",
    version="1.0.0"
)

# Підключаємо роутер з нашими ендпоінтами
app.include_router(router)

# Опціонально: додаємо базовий маршрут для перевірки працездатності
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "Library API is running",
        "docs": "/docs"
    }

# Цей блок дозволяє запускати файл напряму через `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)