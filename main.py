# main.py

# 1. Импортируем класс FastAPI. Аналог: import express from 'express';
from fastapi import FastAPI

# 2. Создаем экземпляр приложения. Аналог: const app = express();
app = FastAPI(
    title="My First API",
    description="This is a demo API for learning FastAPI, created by a Node.js developer!",
    version="0.1.0",
)

# 3. Создаем маршрут (route) для корневого URL.
# Декоратор `@app.get("/")` связывает URL и HTTP-метод GET с функцией ниже.
# Это прямой аналог app.get('/', (req, res) => { ... });
@app.get("/")
def read_root():
    """
    Этот эндпоинт возвращает приветственное сообщение.
    Вся документация из docstring будет видна в /docs!
    """
    # 4. FastAPI автоматически конвертирует словарь Python в JSON-ответ.
    # Аналог: res.json({ "message": "Hello from your first FastAPI server!" });
    return {"message": "Hello from your first FastAPI server!"}

# ... после первого эндпоинта

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """
    Получает товар по его ID.
    - **item_id**: ID товара (обязательный параметр пути).
    - **q**: Поисковый запрос (опциональный параметр запроса).
    """
    # FastAPI автоматически валидирует `item_id`. Если передать не число, будет ошибка.
    # `q` - опциональный параметр. Если его нет, он будет равен `None`.
    # Это похоже на `const { item_id } = req.params; const { q } = req.query;`

    response_data = {"item_id": item_id}
    if q:
        response_data["q"] = q

    return response_data
