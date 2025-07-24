# main.py

# --- Шаг 1: Переменные и базовые типы ---
# Аналог в JS: const projectTitle = 'User Processing Script';
project_title = "Скрипт обработки пользователей"
print(f"--- Запуск: {project_title} ---") # f-строка - это полный аналог template literals `` в JS

# --- Шаг 2: Список словарей (List of Dictionaries) ---
# Аналог в JS: const users = [ { id: 1, name: 'Alice', ... } ];
# Словарь (dict) - это аналог объекта JS. Список (list) - аналог массива.
users = [
    {"id": 1, "name": "Alice", "role": "premium", "logins": 95},
    {"id": 2, "name": "Bob", "role": "free", "logins": 23},
    {"id": 3, "name": "Charlie", "role": "admin", "logins": 150},
    {"id": 4, "name": "Diana", "role": "premium", "logins": 110}
]

# --- Шаг 3: Цикл и условные операторы (for, if/else) ---
# Это самая важная часть. Вместо {} используются отступы.
# Аналог в JS: for (const user of users) { ... }
print("\nАнализ пользователей:")
for user in users:
    # Начало блока 'for'. Все, что с отступом ниже, выполнится в цикле.

    is_premium = user["role"] == "premium"
    is_admin = user["role"] == "admin"

    # Аналог в JS: if (is_premium || is_admin) { ... } else { ... }
    if is_premium or is_admin:
        # Еще один уровень вложенности = еще один отступ.
        greeting = f"✅  Здравствуйте, {user['name']}! Ваш статус: {user['role']}."
        print(greeting)
    else:
        message = f"   Пользователь {user['name']} имеет базовый доступ."
        print(message)

# Код без отступа - конец блока 'for'.
print("\n--- Анализ завершен ---")

# (venv) aaaaa@aaaaa-GF63-Thin-9SCXR:~/AI-TUTORIALS/python-trainings$ python main.py
# --- Запуск: Скрипт обработки пользователей ---

# Анализ пользователей:
# ✅  Здравствуйте, Alice! Ваш статус: premium.
#    Пользователь Bob имеет базовый доступ.
# ✅  Здравствуйте, Charlie! Ваш статус: admin.
# ✅  Здравствуйте, Diana! Ваш статус: premium.

# --- Анализ завершен ---


# --- Задача 2: Pythonic Way ---

# Способ 1: Классический цикл (как в JS с .push())
important_names_classic = []
for user in users:
    if user["role"] == "premium" or user["role"] == "admin":
        important_names_classic.append(user["name"])

print(f"\nИмена важных пользователей (классический способ): {important_names_classic}")


# Способ 2: List Comprehension (аналог filter + map)
# [что_добавить for элемент in список if условие]
important_names_pythonic = [user["name"] for user in users if user["role"] in ("premium", "admin")]

print(f"Имена важных пользователей (Pythonic способ): {important_names_pythonic}")

# Имена важных пользователей (классический способ): ['Alice', 'Charlie', 'Diana']
# Имена важных пользователей (Pythonic способ): ['Alice', 'Charlie', 'Diana']



# --- Задача 3: Функции ---

# Аналог в JS: function getImportantUserNames(userList) { ... }
def get_important_user_names(user_list):
    """
    Это docstring — строка документации. Хорошая практика для описания функции.
    Принимает список пользователей и возвращает список имен премиум-пользователей и админов.
    """
    names = [user["name"] for user in user_list if user["role"] in ("premium", "admin")]
    return names

# Вызываем функцию и передаем ей наш список
# Аналог в JS: const importantUsers = getImportantUserNames(users);
important_users = get_important_user_names(users)

print(f"\nРезультат вызова функции: {important_users}")
print(f"Всего важных пользователей: {len(important_users)}") # len() - аналог .length

# Результат вызова функции: ['Alice', 'Charlie', 'Diana']
# Всего важных пользователей: 3
