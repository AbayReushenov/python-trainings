1. Создайте виртуальное окружение. Назовем его venv.
# Эта команда создает папку 'venv' со всем необходимым
```
python3 -m venv venv
```
2. Активируйте окружение.
```
source venv/bin/activate
```
3.  Создаем requirements.txt (аналог package.json)
Этот файл содержит список всех библиотек, которые нужно установить. Создать его очень просто:

# Команда 'freeze' выводит все установленные в 'venv' пакеты.
# Мы перенаправляем этот вывод в файл requirements.txt.
pip freeze > requirements.txt

4. Содать .gitignore
```
touch .gitignore
```
5. git init

