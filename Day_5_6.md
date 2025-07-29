# Аналогично разработать для дня 5 - 6

ОПИСАНИЕ ЗАДАЧИ:

```
День 5-6: Введение в ООП и работу с внешними библиотеками
Цель: Понять основы объектно-ориентированного программирования в Python и начать использовать сторонние библиотеки.
Материалы: Учебники по ООП в Python, документация по NumPy и Pandas.
Темы:
Классы, объекты, атрибуты, методы.
Наследование и полиморфизм (базовые концепции).
Установка пакетов с помощью pip.
Введение в NumPy: создание массивов, базовые операции.
Введение в Pandas: DataFrame, чтение CSV/JSON.
Практика: Создайте простой класс, который имитирует какую-либо сущность (например, User или Product). Используйте NumPy для выполнения некоторых числовых операций и Pandas для загрузки и базовой обработки небольшого набора данных.
```

Конечно! Мы подошли к очень интересному этапу. Дни 5 и 6 — это мост между написанием скриптов и построением настоящих, масштабируемых приложений. Объектно-ориентированное программирование (ООП) поможет вам организовать логику так же, как вы привыкли делать это в NestJS, а работа с библиотеками данных, такими как Pandas, — это первый шаг к тому, чтобы ваш AI-агент мог работать с реальными наборами данных.

Давайте творчески переосмыслим предложенный план, чтобы он был максимально релевантным для вашей цели.

### Скорректированный план на Дни 5-6

* **День 5: ООП и рефакторинг API.** Мы не просто изучим классы, а сразу применим их для рефакторинга нашего FastAPI-приложения, создав сервисный слой, как в NestJS. Это сделает код чище, более тестируемым и готовым к росту.
* **День 6: Работа с данными с помощью Pandas.** Мы сосредоточимся на Pandas, так как для обработки структурированных данных (CSV, JSON-файлы), с которыми часто работают LLM-агенты, он подходит лучше, чем NumPy. Мы создадим API-эндпоинт, который будет читать и анализировать данные из файла.

**Подготовка:** Давайте зафиксируем в Git всю работу, проделанную в День 4.

```bash
git add .
git commit -m "feat: Complete Day 4 - CRUD operations and async in FastAPI"
```

Теперь мы готовы строить более сложную структуру.

### День 5: ООП — Создание сервисного слоя

**Цель:** Понять основы ООП в Python и применить их для рефакторинга нашего API, вынеся бизнес-логику из эндпоинтов в отдельный сервисный класс.

#### Задача 1: Классы в Python (Ваш `class` в JavaScript)

Давайте начнем с основ. Класс в Python очень похож на класс в ES6.

* **Аналогия**: `class User { constructor(name) { this.name = name; } }` в JS превращается в `class User: def __init__(self, name): self.name = name`.
* **`__init__`**: Это специальный метод-инициализатор, аналог `constructor`. Он вызывается при создании нового объекта (`new User()`).
* **`self`**: Это аналог `this`. `self` — это ссылка на сам экземпляр объекта. В Python его нужно явно передавать первым аргументом во все методы экземпляра.


#### Задача 2: "Сервисный слой" — Рефакторинг CRUD-логики

Сейчас вся наша логика (поиск в списке, добавление, удаление) находится прямо в функциях-эндпоинтах в `main.py`. Это быстро превращается в беспорядок. Давайте создадим `UserService`, который будет инкапсулировать всю работу с пользователями.

1. **Создайте новый файл `services.py`**. В нем будет наш сервисный класс.
2. **Наполните `services.py` кодом**:

```python
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

```

3. **Обновите `main.py` для использования `UserService`**. Теперь ваш `main.py` станет "тонким контроллером", который только принимает запросы и передает их в сервис.

```python
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
```


**Что здесь нового и важного:**

* **Разделение ответственности**: `main.py` отвечает за API (эндпоинты, запросы, ответы), а `services.py` — за бизнес-логику (как хранить и обрабатывать данные).
* **`response_model=list[User]`**: Мы явно указываем FastAPI, какой должна быть структура ответа. Это улучшает документацию и обеспечивает консистентность.
* **`**user_data.model_dump()`**: Это питонический способ "развернуть" словарь в именованные аргументы. `User(id=5, **{"name": "Eve", "role": "guest"})` эквивалентно `User(id=5, name="Eve", role="guest")`.
* **Чистота и тестируемость**: Теперь вы можете тестировать `UserService` отдельно от FastAPI, просто создав его экземпляр и вызывая методы.

Запустите сервер (`uvicorn main:app --reload`) и убедитесь, что все работает как прежде, но код стал гораздо более организованным.

### День 6: Pandas — Ваш швейцарский нож для данных

**Цель:** Научиться использовать библиотеку Pandas для чтения и базового анализа структурированных данных (CSV) и интегрировать это в наше API.

#### Задача 1: Установка и знакомство с Pandas

1. **Установите Pandas**. Pandas не входит в стандартную библиотеку, поэтому его нужно установить.

```bash
pip install pandas
```

И сразу обновите ваши зависимости:

```bash
pip freeze > requirements.txt
```

2. **Создайте файл с данными**. Создайте в корне проекта файл `users_data.csv` со следующим содержимым. Это будет наш источник данных.

```csv
id,name,role,signup_date,last_login_days_ago
101,Frank,premium,2024-01-15,5
102,Grace,free,2024-03-22,80
103,Heidi,premium,2023-11-10,2
104,Ivan,admin,2023-05-20,1
105,Judy,free,2024-07-21,30
```


#### Задача 2: Чтение и анализ CSV с помощью Pandas

Создайте новый файл `data_analyzer.py`, чтобы поэкспериментировать с Pandas.

```python
# data_analyzer.py

import pandas as pd

def analyze_user_data(filepath: str):
    """
    Читает CSV-файл с данными пользователей и выполняет базовый анализ.
    """
    try:
        # 1. Чтение CSV в DataFrame
        # DataFrame - это основная структура данных в Pandas, похожая на таблицу или лист Excel.
        df = pd.read_csv(filepath)
        print("--- Данные успешно загружены ---")
        print(df.head()) # .head() показывает первые 5 строк

        # 2. Базовая информация о данных
        print("\n--- Информация о DataFrame ---")
        df.info() # Показывает типы данных, количество непустых значений

        # 3. Базовый анализ - фильтрация
        # Аналог SQL: SELECT * FROM users WHERE role = 'premium';
        premium_users = df[df['role'] == 'premium']
        print("\n--- Премиум-пользователи ---")
        print(premium_users)

        # 4. Простая аналитика
        average_days_since_login = df['last_login_days_ago'].mean()
        print(f"\nСреднее количество дней с последнего логина: {average_days_since_login:.2f}")

        # 5. Возвращаем результат в формате, удобном для API (список словарей)
        return df.to_dict('records')

    except FileNotFoundError:
        print(f"Ошибка: файл не найден по пути {filepath}")
        return None

if __name__ == "__main__":
    analyze_user_data("users_data.csv")
```

Запустите этот скрипт напрямую (`python data_analyzer.py`), чтобы увидеть, как Pandas читает и анализирует файл.

#### Задача 3: Интеграция Pandas в FastAPI

Теперь давайте создадим новый эндпоинт в `main.py`, который будет использовать наш анализатор.

1. **Импортируйте `data_analyzer` в `main.py`**:
`from data_analyzer import analyze_user_data`
2. **Добавьте новый эндпоинт в `main.py`**:

```python
# ... в конце файла main.py

@app.get("/analytics/users-from-csv")
def get_users_from_csv():
    """
    Читает данные пользователей из CSV-файла и возвращает их в виде JSON.
    """
    # В реальном приложении путь к файлу лучше вынести в конфигурацию
    filepath = "users_data.csv"
    data = analyze_user_data(filepath)
    if data is None:
        raise HTTPException(status_code=500, detail="Could not analyze data file.")

    return {"source": "csv", "data": data}
```


Запустите сервер и перейдите на `http://127.0.0.1:8000/docs`. Вы увидите новый эндпоинт. Выполните его, и вы получите JSON-ответ с данными, которые Pandas прочитал из CSV-файла!

### Итог Дней 5-6

Вы сделали огромный шаг от написания скриптов к архитектуре приложений:

* Вы освоили **классы** в Python и применили их для создания **сервисного слоя**, что является стандартной практикой в больших приложениях.
* Ваш код стал **чище, организованнее и проще для тестирования**.
* Вы научились использовать **Pandas**, одну из самых мощных библиотек Python, для чтения и базового анализа табличных данных.
* Вы успешно **интегрировали внешнюю библиотеку для обработки данных в ваше FastAPI-приложение**.

Теперь у вас есть прочный фундамент: структурированный бэкенд, способный работать как с простой логикой, так и с внешними наборами данных. Вы полностью готовы к следующему шагу — интеграции LangChain и созданию вашего первого LLM-агента.

