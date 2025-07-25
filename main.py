# main.py

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="User Management API",
    description="An API to manage users, built with FastAPI.",
    version="1.0.0",
)

# --- База данных (в виде простого списка словарей) ---
# В реальном проекте это будет идти из PostgreSQL, MongoDB и т.д.
DB_USERS = [
    {"id": 1, "name": "Alice", "role": "premium"},
    {"id": 2, "name": "Bob", "role": "free"},
    {"id": 3, "name": "Charlie", "role": "admin"},
    {"id": 4, "name": "Diana", "role": "premium"},
]

# --- Эндпоинты ---

@app.get("/")
def read_root():
    """Корневой эндпоинт с приветствием."""
    return {"message": "Welcome to the User Management API!"}


@app.get("/users")
def get_all_users():
    """Возвращает список всех пользователей в системе."""
    return {"users": DB_USERS}


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    """
    Находит и возвращает одного пользователя по его ID.
    Если пользователь не найден, возвращает ошибку 404.
    """
    # Используем 'list comprehension' из Дня 1, но можно и простой цикл
    found_user = next((user for user in DB_USERS if user["id"] == user_id), None)

    if not found_user:
        # Аналог: return res.status(404).json({ message: "User not found" });
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )

    return {"user": found_user}

