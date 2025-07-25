# main.py

# --- Шаг 1: Определение функций ---

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

    print("\n--- Анализ завершен ---")


# --- Шаг 2: Точка входа в скрипт ---
# Эта конструкция гарантирует, что код внутри `main()` будет вызван
# только при прямом запуске файла `python main.py`.
# Это стандартная и очень распространенная практика в Python.
if __name__ == "__main__":
    main()

# --- Запуск: Скрипт обработки пользователей v2.0 ---

# Анализ пользователей:
# ✅  Здравствуйте, Alice! Ваш статус: premium.
#     Пользователь Bob имеет базовый доступ.
# ✅  Здравствуйте, Charlie! Ваш статус: admin.
# ✅  Здравствуйте, Diana! Ваш статус: premium.

# Список важных пользователей: ['Alice', 'Charlie', 'Diana']

# --- Анализ завершен ---
