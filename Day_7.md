# День 7: Подготовка к работе с LangChain - От FastAPI к AI-агентам

Отлично! День 7 — это кульминация нашего недельного путешествия. Мы подошли к моменту, когда вся ваша подготовка сливается воедино, и вы готовы делать следующий шаг: от создания обычных веб-API к построению интеллектуальных LLM-агентов.

Сегодня мы не просто изучим LangChain — мы интегрируем его с вашим FastAPI-приложением, создав полноценный AI-powered сервис.

### Подготовительный этап: Закрепление достижений

Давайте зафиксируем всю работу Дней 5-6 в Git:

```bash
git add .
git commit -m "feat: Complete Days 5-6 - OOP refactoring and Pandas integration"
```


## План на День 7: От HTTP API к AI-агенту

### Задача 1: Установка и подготовка LangChain-экосистемы

Сначала нам нужно правильно установить LangChain и подготовить всё необходимое для работы с LLM-провайдерами.

1. **Установка LangChain и зависимостей**. LangChain — это не одна библиотека, а целая экосистема пакетов.

```bash
# Основные пакеты LangChain
pip install langchain
pip install langchain-core
pip install langchain-community

# Интеграция с OpenAI (самый популярный провайдер)
pip install langchain-openai

# Интеграция с Anthropic Claude (альтернатива OpenAI)
pip install langchain-anthropic

# Для работы с векторными базами данных (нужно для RAG)
pip install langchain-chroma
```

И обязательно обновите ваши зависимости:

```bash
pip freeze > requirements.txt
```

2. **Настройка API-ключей**. Для работы с LLM вам понадобится API-ключ от одного из провайдеров.

**Вариант 1: OpenAI (рекомендуется для начала)**
    - Перейдите на [platform.openai.com](https://platform.openai.com)
    - Создайте аккаунт и получите API-ключ
    - **Важно**: Убедитесь, что у вас есть средства на счету для API-вызовов

**Вариант 2: Anthropic Claude (бесплатная альтернатива)**
    - Перейдите на [console.anthropic.com](https://console.anthropic.com/)
    - Claude предоставляет более щедрый бесплатный лимит

**Создайте файл `.env`** в корне проекта:

```env
# .env
OPENAI_API_KEY=sk-your-openai-key-here
# или
ANTHROPIC_API_KEY=your-anthropic-key-here
```

**Установите python-dotenv** для загрузки переменных окружения:

```bash
pip install python-dotenv
```


### Задача 2: Первый LLM-вызов в Python

Давайте создадим новый файл `llm_demo.py` и познакомимся с основными компонентами LangChain[^6][^7][^8].

```python
# llm_demo.py

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# === Компонент 1: MODELS (Модели) ===
# Модели - это обёртки вокруг LLM-провайдеров

# Вариант 1: OpenAI
from langchain_openai import ChatOpenAI

openai_llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # Можно использовать gpt-4 если есть доступ
    temperature=0.7,        # Креативность: 0 = детерминированно, 1 = очень креативно
    api_key=os.getenv("OPENAI_API_KEY")  # Ключ из .env файла
)

# Вариант 2: Anthropic Claude (раскомментируйте если используете)
# from langchain_anthropic import ChatAnthropic
# claude_llm = ChatAnthropic(
#     model="claude-3-sonnet-20240229",
#     api_key=os.getenv("ANTHROPIC_API_KEY")
# )

# === Компонент 2: PROMPTS (Шаблоны промптов) ===
from langchain_core.prompts import ChatPromptTemplate

# Создаем шаблон промпта с переменными
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Вы опытный Python-разработчик и ментор. Отвечайте кратко и по делу."),
    ("human", "Объясните концепцию: {concept}")
])

# === Компонент 3: OUTPUT PARSERS (Парсеры вывода) ===
from langchain_core.output_parsers import StrOutputParser

# Простейший парсер - преобразует ответ LLM в строку
string_parser = StrOutputParser()

# === Создание цепочки (CHAIN) ===
# Это ключевая концепция LangChain - связывание компонентов в pipeline
# Аналог: prompt -> LLM -> parser (как конвейер в Unix: cmd1 | cmd2 | cmd3)

llm_chain = prompt_template | openai_llm | string_parser

# === Тестирование нашей первой LLM-цепочки ===
def test_basic_chain():
    print("=== Тест базовой LLM-цепочки ===")

    # Вызываем нашу цепочку с конкретными данными
    response = llm_chain.invoke({"concept": "list comprehensions в Python"})

    print("Ответ от LLM:")
    print(response)
    print("-" * 50)

# === Пример более сложного промпта ===
code_review_prompt = ChatPromptTemplate.from_messages([
    ("system", """Вы эксперт по code review. Проанализируйте код и дайте:
    1. Краткую оценку качества (1-10)
    2. Основные проблемы (если есть)
    3. Одно конкретное улучшение"""),
    ("human", "Код для анализа:\n{code}")
])

code_review_chain = code_review_prompt | openai_llm | string_parser

def test_code_review():
    print("=== Тест code review цепочки ===")

    sample_code = """
def process_users(users):
    result = []
    for user in users:
        if user['age'] > 18:
            result.append(user['name'].upper())
    return result
    """

    response = code_review_chain.invoke({"code": sample_code})
    print("Code Review:")
    print(response)
    print("-" * 50)

# === RAG концепция: подготовка к работе с внешними данными ===
def explain_rag_concept():
    print("=== Объяснение RAG (Retrieval-Augmented Generation) ===")

    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", "Объясните техническую концепцию простыми словами с примером."),
        ("human", "Что такое RAG и как это поможет в создании AI-агентов?")
    ])

    rag_chain = rag_prompt | openai_llm | string_parser

    response = rag_chain.invoke({})
    print("Объяснение RAG:")
    print(response)
    print("-" * 50)

if __name__ == "__main__":
    # Проверяем, что API-ключ настроен
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Ошибка: Не найден API-ключ!")
        print("Создайте файл .env и добавьте ваш OPENAI_API_KEY или ANTHROPIC_API_KEY")
        exit(1)

    print("✅ LangChain готов к работе!")

    # Запускаем тесты
    test_basic_chain()
    test_code_review()
    explain_rag_concept()
```

Запустите этот скрипт:

```bash
python llm_demo.py
```

**Что здесь происходит:**

* **Models**: Мы настроили подключение к LLM-провайдеру (OpenAI или Claude)
* **Prompts**: Создали шаблоны с переменными для разных задач
* **Parsers**: Настроили обработку ответов от LLM
* **Chains**: Связали всё в единые пайплайны с помощью оператора `|`


### Задача 3: Интеграция LangChain с FastAPI

Теперь самое интересное — давайте интегрируем наши LLM-возможности в FastAPI-приложение, создав полноценный AI-powered API.

**Создайте новый файл `ai_main.py`:**

```python
# ai_main.py

import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Загружаем переменные окружения
load_dotenv()

# Импортируем наш UserService из предыдущих дней
from services import UserService

app = FastAPI(
    title="AI-Powered User Management API",
    description="FastAPI + LangChain: Управление пользователями с AI-помощником",
    version="3.0.0",
)

# === Настройка LLM ===
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3,  # Менее креативно для деловых задач
    api_key=os.getenv("OPENAI_API_KEY")
)

# === Pydantic модели для API ===
class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"

class ChatRequest(BaseModel):
    message: str
    context: str = ""

class UserAnalysisRequest(BaseModel):
    user_data: list[dict]

# === LangChain цепочки для разных задач ===

# 1. Code Review AI
code_review_prompt = ChatPromptTemplate.from_messages([
    ("system", """Вы эксперт по code review для языка {language}.
    Проанализируйте код и верните JSON со следующей структурой:
    {{
        "score": число от 1 до 10,
        "issues": ["список проблем"],
        "improvements": ["список улучшений"],
        "summary": "краткое резюме"
    }}"""),
    ("human", "Код для анализа:\n{code}")
])

code_review_chain = code_review_prompt | llm | StrOutputParser()

# 2. User Analysis AI
user_analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """Проанализируйте данные пользователей и дайте краткие инсайты:
    - Общую статистику
    - Основные паттерны
    - Рекомендации по улучшению"""),
    ("human", "Данные пользователей: {user_data}")
])

user_analysis_chain = user_analysis_prompt | llm | StrOutputParser()

# 3. General AI Assistant
assistant_prompt = ChatPromptTemplate.from_messages([
    ("system", """Вы AI-ассистент для разработчиков. Отвечайте кратко и по делу.
    Контекст: {context}"""),
    ("human", "{message}")
])

assistant_chain = assistant_prompt | llm | StrOutputParser()

# === Создаем сервисы ===
user_service = UserService()

# === API Эндпоинты ===

@app.get("/")
async def root():
    return {
        "message": "🤖 AI-Powered User Management API готов к работе!",
        "features": [
            "/ai/code-review - Анализ кода с помощью AI",
            "/ai/analyze-users - Анализ пользователей с помощью AI",
            "/ai/chat - Общий AI-ассистент",
            "/users - Все обычные CRUD операции"
        ]
    }

# === AI-эндпоинты ===

@app.post("/ai/code-review")
async def ai_code_review(request: CodeReviewRequest):
    """
    Анализирует предоставленный код с помощью AI и возвращает рекомендации.
    """
    try:
        analysis = await code_review_chain.ainvoke({
            "code": request.code,
            "language": request.language
        })
        return {
            "analysis": analysis,
            "language": request.language,
            "timestamp": "now"  # В реальном приложении используйте datetime
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

@app.post("/ai/analyze-users")
async def ai_analyze_users(request: UserAnalysisRequest):
    """
    Анализирует данные пользователей с помощью AI и предоставляет инсайты.
    """
    try:
        analysis = await user_analysis_chain.ainvoke({
            "user_data": str(request.user_data)
        })
        return {
            "insights": analysis,
            "total_users": len(request.user_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

@app.post("/ai/chat")
async def ai_chat(request: ChatRequest):
    """
    Общий AI-ассистент для разработчиков.
    """
    try:
        response = await assistant_chain.ainvoke({
            "message": request.message,
            "context": request.context
        })
        return {
            "response": response,
            "context": request.context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI chat failed: {str(e)}")

# === Эндпоинт, который объединяет пользователей и AI ===

@app.get("/ai/smart-user-insights")
async def smart_user_insights():
    """
    Получает всех пользователей из сервиса и анализирует их с помощью AI.
    """
    try:
        # Получаем данные пользователей из нашего сервиса
        users = user_service.get_all_users()

        # Анализируем с помощью AI
        analysis = await user_analysis_chain.ainvoke({
            "user_data": str(users)
        })

        return {
            "users": users,
            "ai_insights": analysis,
            "total_users": len(users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Smart analysis failed: {str(e)}")

# === Обычные CRUD эндпоинты (из предыдущих дней) ===

@app.get("/users")
async def get_all_users():
    return {"users": user_service.get_all_users()}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return {"user": user_service.get_user_by_id(user_id)}

# И так далее... (остальные CRUD операции)

if __name__ == "__main__":
    # Проверяем настройки
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Не найден OPENAI_API_KEY в файле .env")
        exit(1)

    print("🚀 Запуск AI-powered FastAPI приложения...")
    print("📖 Документация: http://127.0.0.1:8000/docs")

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Запустите новое приложение:

```bash
python ai_main.py
```


### Задача 4: Понимание RAG и подготовка к продвинутым AI-агентам

RAG (Retrieval-Augmented Generation) — это техника, которая позволяет LLM использовать внешние источники данных для генерации более точных ответов[^9][^10][^11].

**Создайте файл `rag_demo.py`** для демонстрации основ RAG:

```python
# rag_demo.py

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

# === Создаем простую "базу знаний" ===
knowledge_base = """
FastAPI - это современный веб-фреймворк для создания API на Python.
Основные преимущества FastAPI:
- Высокая производительность
- Автоматическая генерация документации
- Поддержка асинхронности
- Встроенная валидация данных с Pydantic

LangChain - это фреймворк для создания приложений с LLM.
Основные компоненты LangChain:
- Models: интеграция с различными LLM
- Prompts: шаблоны для промптов
- Chains: связывание компонентов
- Agents: автономные AI-агенты

Pandas - библиотека для анализа данных в Python.
Основные возможности Pandas:
- Работа с DataFrame и Series
- Чтение различных форматов данных
- Группировка и агрегация данных
- Обработка пропущенных значений
"""

class SimpleRAG:
    def __init__(self, knowledge_base: str):
        self.knowledge_base = knowledge_base
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,  # Низкая температура для фактической точности
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Промпт для RAG
        self.rag_prompt = ChatPromptTemplate.from_messages([
            ("system", """Используйте предоставленный контекст для ответа на вопрос.
            Если в контексте нет информации для ответа, так и скажите.

            Контекст: {context}"""),
            ("human", "Вопрос: {question}")
        ])

        self.rag_chain = self.rag_prompt | self.llm | StrOutputParser()

    def search_relevant_info(self, query: str) -> str:
        """
        Простой поиск релевантной информации в базе знаний.
        В реальном RAG здесь был бы векторный поиск.
        """
        query_lower = query.lower()
        lines = self.knowledge_base.split('\n')

        relevant_lines = []
        for line in lines:
            if any(keyword in line.lower() for keyword in query_lower.split()):
                relevant_lines.append(line)

        return '\n'.join(relevant_lines) if relevant_lines else "Информация не найдена."

    async def ask(self, question: str) -> str:
        """
        Основной метод RAG: поиск + генерация ответа.
        """
        # 1. Retrieval: поиск релевантной информации
        context = self.search_relevant_info(question)

        # 2. Augmented Generation: генерация ответа с контекстом
        response = await self.rag_chain.ainvoke({
            "context": context,
            "question": question
        })

        return response

async def demo_rag():
    print("=== Демонстрация простого RAG ===")

    rag = SimpleRAG(knowledge_base)

    questions = [
        "Что такое FastAPI?",
        "Какие основные компоненты LangChain?",
        "Как работает Pandas?",
        "Что такое Docker?"  # Вопрос, на который нет ответа в базе
    ]

    for question in questions:
        print(f"\n❓ Вопрос: {question}")
        answer = await rag.ask(question)
        print(f"🤖 Ответ: {answer}")
        print("-" * 50)

if __name__ == "__main__":
    import asyncio

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Не найден OPENAI_API_KEY")
        exit(1)

    asyncio.run(demo_rag())
```

Запустите RAG демо:

```bash
python rag_demo.py
```


## Итог Дня 7: Что вы достигли

🎉 **Поздравляю! Вы успешно завершили недельный интенсив по Python и LangChain!**

**Что вы освоили:**

1. **LangChain экосистему**: установили и настроили основные компоненты
2. **Базовые концепции**: Models, Prompts, Parsers, Chains
3. **Интеграцию с FastAPI**: создали AI-powered веб-сервис
4. **Основы RAG**: поняли, как LLM может работать с внешними данными
5. **Практические навыки**: готовый код для создания AI-агентов

**Ваш технологический стек теперь включает:**

- ✅ Python (синтаксис, ООП, модули)
- ✅ FastAPI (веб-API, асинхронность)
- ✅ Pandas (анализ данных)
- ✅ LangChain (LLM-интеграции)
- ✅ Git (версионирование)
- ✅ Виртуальные окружения (изоляция проектов)


## Следующие шаги: Путь к продвинутым AI-агентам

Теперь у вас есть прочный фундамент для создания LLM-агентов. Вот куда двигаться дальше:

### Неделя 2: Продвинутые возможности

- **LangChain Agents**: автономные агенты с инструментами
- **Vector Databases**: Chroma, Pinecone для продвинутого RAG
- **Memory Systems**: сохранение контекста между сессиями
- **LangSmith**: отладка и мониторинг AI-приложений


### Неделя 3: Продакшн-готовые решения

- **Docker**: контейнеризация AI-приложений
- **Streaming**: потоковые ответы от LLM
- **Rate Limiting**: ограничение запросов к AI
- **Error Handling**: надёжная обработка ошибок LLM

Вы готовы создавать настоящие AI-продукты! 🚀

<div style="text-align: center">⁂</div>
