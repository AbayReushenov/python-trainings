# main.py

from fastapi import FastAPI
from pydantic import BaseModel

# Импортируем наш новый сервис
from services import UserService

app = FastAPI(
    title="User Management API v2.0 (with Service Layer)",
    version="2.0.0",
)

# Создаем один экземпляр нашего сервиса
# В NestJS это было бы сделано через Dependency Injection
user_service = UserService()

# --- Схемы данных (Pydantic Models) ---
class User(BaseModel):
    id: int
    name: str
    role: str

class CreateUserRequest(BaseModel):
    name: str
    role: str

# --- Эндпоинты ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API v2.0!"}

@app.get("/users", response_model=list[User])
def get_all_users():
    return user_service.get_all_users()

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    return user_service.get_user_by_id(user_id)

@app.post("/users", response_model=User, status_code=201)
def create_user(user_data: CreateUserRequest):
    # Создаем полную модель User, т.к. ID генерируется в сервисе
    full_user_data = User(id=user_service.next_user_id, **user_data.model_dump())
    return user_service.create_user(full_user_data)

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: CreateUserRequest):
    full_user_data = User(id=user_id, **user_data.model_dump())
    return user_service.update_user(user_id, full_user_data)

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return user_service.delete_user(user_id)
