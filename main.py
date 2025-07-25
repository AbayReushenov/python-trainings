# main.py

# В самом верху файла добавьте импорт
# Аналог: import requests from 'requests'; (хотя синтаксис проще)
import requests

def process_users(user_list):
    """
    Анализирует список пользователей, выводит приветствия для "важных"
    и возвращает список их имен.

    Аналог в JS: const processUsers = (userList) => { ... };
    """
    print("\nАнализ пользователей:")

    important_names = []
    for user in user_list:
        is_premium = user["role"] == "premium"
        is_admin = user["role"] == "admin"

        if is_premium or is_admin:
            greeting = f"✅  Здравствуйте, {user['name']}! Ваш статус: {user['role']}."
            print(greeting)
            important_names.append(user["name"]) # .append - это аналог .push()
        else:
            message = f"   Пользователь {user['name']} имеет базовый доступ."
            print(message)

    return important_names

def get_random_data():
    """
    Делает GET-запрос к публичному API и возвращает данные.
    """
    print("\nПолучение внешних данных...")
    api_url = "https://jsonplaceholder.typicode.com/todos/1" # Простое JSON API для примера

    # try...except: Блок для обработки ошибок. Это аналог try...catch в JS.
    # Если что-то пойдет не так с запросом (нет сети, сервер вернул ошибку 500), выполнение перейдет в блок except.
    try:
        # Аналог: const response = await axios.get(api_url);
        response = requests.get(api_url)

        # Проверяем, что запрос прошел успешно (статус 2xx)
        response.raise_for_status() # Если статус 4xx или 5xx, вызовет ошибку
        # response.raise_for_status(): Удобный метод, который проверяет код ответа. Если код 200-299, он ничего не делает.
        # Если это код ошибки (4xx, 5xx), он генерирует исключение, которое будет поймано нашим except.

        # .json() парсит JSON-ответ в питоновский словарь (dict)
        # Аналог: const data = response.data;
        data = response.json()
        print("✅ Данные с API успешно получены!")
        return data

    except requests.exceptions.RequestException as e:
        # Обработка ошибок сети, таймаутов и т.д.
        print(f"❌ Ошибка при запросе к API: {e}")
        return None

def main():
    """
    Главная функция, точка входа в нашу программу.
    """
    project_title = "Скрипт обработки пользователей v2.0"
    print(f"--- Запуск: {project_title} ---")

    users = [
        {"id": 1, "name": "Alice", "role": "premium", "logins": 95},
        {"id": 2, "name": "Bob", "role": "free", "logins": 23},
        {"id": 3, "name": "Charlie", "role": "admin", "logins": 150},
        {"id": 4, "name": "Diana", "role": "premium", "logins": 110}
    ]

    # Вызываем нашу первую функцию и сохраняем результат
    processed_names = process_users(users)
    print(f"\nСписок важных пользователей: {processed_names}")

    # Вызываем нашу новую функцию
    external_data = get_random_data()
    if external_data:
    # Работаем с полученными данными
        title = external_data.get("title", "Заголовок не найден")
        print(f"Полученный заголовок из API: '{title}'")

    print("\n--- Анализ завершен ---")


# --- Шаг 2: Точка входа в скрипт ---
# Эта конструкция гарантирует, что код внутри `main()` будет вызван
# только при прямом запуске файла `python main.py`.
# Это стандартная и очень распространенная практика в Python.
if __name__ == "__main__":
    main()

# (venv) aaaaa@aaaaa-GF63-Thin-9SCXR:~/AI-TUTORIALS/python-trainings$ python main.py
# --- Запуск: Скрипт обработки пользователей v2.0 ---

# Анализ пользователей:
# ✅  Здравствуйте, Alice! Ваш статус: premium.
#    Пользователь Bob имеет базовый доступ.
# ✅  Здравствуйте, Charlie! Ваш статус: admin.
# ✅  Здравствуйте, Diana! Ваш статус: premium.

# Список важных пользователей: ['Alice', 'Charlie', 'Diana']

# Получение внешних данных...
# ❌ Ошибка при запросе к API: HTTPSConnectionPool(host='api.jsonserve.com', port=443): Max retries exceeded with url: /bRZJAw (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7fb91fcb29f0>: Failed to resolve 'api.jsonserve.com' ([Errno -2] Name or service not known)"))

# --- Анализ завершен ---
# (venv) aaaaa@aaaaa-GF63-Thin-9SCXR:~/AI-TUTORIALS/python-trainings$ python main.py
# --- Запуск: Скрипт обработки пользователей v2.0 ---

# Анализ пользователей:
# ✅  Здравствуйте, Alice! Ваш статус: premium.
#    Пользователь Bob имеет базовый доступ.
# ✅  Здравствуйте, Charlie! Ваш статус: admin.
# ✅  Здравствуйте, Diana! Ваш статус: premium.

# Список важных пользователей: ['Alice', 'Charlie', 'Diana']

# Получение внешних данных...
# ✅ Данные с API успешно получены!
# Полученный заголовок из API: 'delectus aut autem'

# --- Анализ завершен ---
# (venv) aaaaa@aaaaa-GF63-Thin-9SCXR:~/AI-TUTORIALS/python-trainings$
