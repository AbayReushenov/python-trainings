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
