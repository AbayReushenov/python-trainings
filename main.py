# main.py

import asyncio # Добавьте этот импорт в самом начале файла
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel # Импортируем BaseModel

# Определяем схему для пользователя
# Аналог: interface User { id: number; name: string; role: string; }
class User(BaseModel):
    id: int
    name: str
    role: str

app = FastAPI(
    title="User Management API",
    description="An API to manage users, built with FastAPI.",
    version="1.0.0",
)

# --- База данных (в виде простого списка словарей) ---
# В реальном проекте это будет идти из PostgreSQL, MongoDB и т.д.
# Изменяем нашу "базу данных"
# Добавляем следующий ID для нового пользователя
next_user_id = 5

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
async def get_all_users(): # Добавляем async перед def
    """
    Возвращает список всех пользователей в системе с имитацией задержки.
    """
    print("Начинаем получать пользователей...")
    await asyncio.sleep(2) # Имитация длительной операции (например, запроса к БД)
    print("Пользователи получены!")
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

# --- Создание пользователя ---
# user: User: FastAPI автоматически ожидает JSON-тело запроса,
# валидирует его по схеме User (через Pydantic) и преобразует в объект User.
# Если JSON не соответствует схеме, вы получите красивую ошибку 422 Unprocessable Entity автоматически.
@app.post("/users/")
def create_user(user: User):
    """
    Создает нового пользователя.
    - **user**: Объект пользователя, который будет автоматически валидирован.
    """
    global next_user_id # Заявляем, что мы будем изменять глобальную переменную
    # global next_user_id: В Python, чтобы изменить глобальную переменную внутри функции,
    # нужно использовать ключевое слово global. Иначе Python создаст новую локальную переменную.

    # Проверяем, существует ли пользователь с таким ID (простая проверка)
    if any(u["id"] == user.id for u in DB_USERS):
        raise HTTPException(status_code=400, detail=f"User with ID {user.id} already exists")

    DB_USERS.append(user.model_dump()) # Pydantic model_dump() конвертирует в dict
    # user.model_dump():
    # Метод Pydantic модели, который конвертирует объект модели обратно в обычный Python-словарь (dict),
    # чтобы его можно было добавить в наш DB_USERS.
    next_user_id += 1
    return {"message": "User created successfully", "user": user}

# Эндпоинт PUT: Обновление пользователя
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user_data: User):
    """
    Обновляет данные существующего пользователя по ID.
    """
    # Используем enumerate() для получения индекса и значения пользователя одновременно.
    # index: Индекс текущего элемента в списке.
    # user: Значение текущего элемента в списке.
    # DB_USERS[index] = updated_user_data.model_dump():
    # Обновляем значение пользователя в списке по индексу.
    # updated_user_data.model_dump():
    # Метод Pydantic модели, который конвертирует объект модели обратно в обычный Python-словарь (dict),
    # чтобы его можно было добавить в наш DB_USERS.
    for index, user in enumerate(DB_USERS):
        if user["id"] == user_id:
            DB_USERS[index] = updated_user_data.model_dump()
            return {"message": "User updated successfully", "user": updated_user_data}
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

# Эндпоинт DELETE: Удаление пользователя
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Удаляет пользователя по ID.
    """
    global DB_USERS # Нужно для модификации списка
    initial_len = len(DB_USERS)
    # Сохраняем длину списка перед удалением.
    DB_USERS = [user for user in DB_USERS if user["id"] != user_id]
    # DB_USERS = [user for user in DB_USERS if user["id"] != user_id]:

    # Фильтруем список, оставляя только пользователей с другими ID.
    # len(DB_USERS) == initial_len:
    # Проверяем, что длина списка не изменилась, чтобы убедиться, что пользователь был удален.
    if len(DB_USERS) == initial_len:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return {"message": "User deleted successfully", "user_id": user_id}

# --- Дополнительные темы Python ---

def flexible_printer(*args, **kwargs):
    """
    Демонстрирует *args (позиционные аргументы) и **kwargs (именованные аргументы).
    Аналог в JS: function flexiblePrinter(...args) { ... } (для args)
    и function flexiblePrinter(options) { ... } (для kwargs, где options - объект)
    """
    print("\n--- Flexible Printer Demo ---")
    print("Позиционные аргументы (*args):", args) # args будет кортежем (tuple)
    print("Именованные аргументы (**kwargs):", kwargs) # kwargs будет словарем (dict)

    for key, value in kwargs.items(): # Итерация по элементам словаря
        print(f"  {key}: {value}")

# Примеры вызова
flexible_printer(1, 2, "hello")
flexible_printer("Python", language="Python", framework="FastAPI", learned_days=4)
flexible_printer(10, count=5, type="number")


# Лямбда-функции
# Аналог в JS: const multiply = (a, b) => a * b;
multiply = lambda a, b: a * b

print("\n--- Lambda Function Demo ---")
print(f"5 * 3 = {multiply(5, 3)}")

# Лямбды часто используются с функциями высшего порядка (map, filter, sorted)
numbers = [1, 5, 2, 8, 3]
# Отсортируем список чисел по их остатку от деления на 3
sorted_numbers = sorted(numbers, key=lambda x: x % 3)
print(f"Исходные числа: {numbers}")
print(f"Отсортированные по остатку от деления на 3: {sorted_numbers}")
