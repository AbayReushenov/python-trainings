# services.py

from fastapi import HTTPException

# Мы будем использовать Pydantic-модель, чтобы указать тип данных
# Но чтобы избежать циклического импорта, мы будем использовать строковые аннотации
# Это продвинутая, но очень полезная техника

class UserService:
    def __init__(self):
        # В реальном приложении здесь было бы подключение к базе данных
        # self.db_connection = ...
        self.db = [
            {"id": 1, "name": "Alice", "role": "premium"},
            {"id": 2, "name": "Bob", "role": "free"},
            {"id": 3, "name": "Charlie", "role": "admin"},
            {"id": 4, "name": "Diana", "role": "premium"},
        ]
        self.next_user_id = 5

    def get_all_users(self):
        return self.db

    def get_user_by_id(self, user_id: int):
        user = next((user for user in self.db if user["id"] == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return user

    def create_user(self, user_data): # user_data будет Pydantic моделью
        if any(u["id"] == user_data.id for u in self.db):
            raise HTTPException(status_code=400, detail=f"User with ID {user_data.id} already exists")

        new_user = user_data.model_dump()
        self.db.append(new_user)
        self.next_user_id += 1
        return new_user

    def update_user(self, user_id: int, user_data):
        for i, user in enumerate(self.db):
            if user["id"] == user_id:
                updated_user = user_data.model_dump()
                self.db[i] = updated_user
                return updated_user
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    def delete_user(self, user_id: int):
        initial_len = len(self.db)
        self.db = [user for user in self.db if user["id"] != user_id]
        if len(self.db) == initial_len:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return {"message": "User deleted successfully", "user_id": user_id}

