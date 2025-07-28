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

