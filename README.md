# FastAPI-проект "ToDoApp"
_с демонcтрацией работы контейнерезации, кэширования, инъекции зависимостей_

**Стек технологий**:
- Python 3.11.6
- FastAPI 0.115.6
- Redis 5.2.1
- SQLAlchemy 2.0.36
- Docker
- flake8
- mypy
- WSL

### Как запустить проект:
При использовании IDE PyCharm клонирование репозитория, установка виртуального окружения и зависимостей выполняется
посредством интерфейса IDE. При использовании IDE VSCode и WSL потребуется выполнить следующие команды
(ниже приводятся команды для Linux):
- Клонировать репозиторий:
```commandline
git clone git@github.com:LeoNefesch/fastapi_crud_todo.git
```
- Зайти в директорию, установить и активировать виртуальное окружение:
```commandline
cd fastapi_crud_todo
```
```commandline
python3 -m venv .venv
```
```commandline
source .venv/bin/activate
```
- Установить зависимости из файла requirements.txt:
```commandline
python3 -m pip install --upgrade pip
```
```commandline
pip install -r requirements.txt
```
- В головной директории проекта создать файл `.env` для локальной разработки и `.env.docker` для работы проекта в
контейнерах:
Файл `.env` должен содержать следующие переменные окружения:
```
ENVIRONMENT=development
DATABASE_URL=sqlite:///./db/todo.db
REDIS_LOGGING_URL=redis://localhost:6379/0
REDIS_CACHING_URL=redis://localhost:6379/1
REDIS_PORT=6379
PORT=8000
DEBUG=True # переключите на False для продакшна
```
Файл `.env.docker` должен содержать следующие переменные окружения:
```
DATABASE_URL=sqlite:///./db/todo.db
REDIS_LOGGING_URL=redis://redis:6379/0
REDIS_CACHING_URL=redis://redis:6379/1
REDIS_PORT=6379
PORT=8000
DEBUG=True # переключите на False для продакшна
```

## Запуск проекта локально
Все команды выполняются из корня проекта.
- Redis (в одной консоли WSL):
```commandline
sudo docker-compose up redis -d
```
- FastAPI (в другой консоли) (или через runner IDE - запуск файла main.py):
```commandline
python main.py
```
Команда для WSL будет такой:
```commandline
python3 main.py
```
- Работа с api-методами:

В браузере перейдите по ссылке `http://127.0.0.1:8001/docs`

Информацию о логировании и кэшировании можно получить через консоль redis (_команды выполняются в WSL_). В db=0
находятся логи redis, в db=1 - результаты кэширования.
```
redis-cli
127.0.0.1:6379> SELECT 0
127.0.0.1:6379> LRANGE http_logs 0 -1
127.0.0.1:6379> SELECT 1
127.0.0.1:6379> GET todos:all
```
Также логи можно найти в директории [logs/](logs) проекта.
### Codestyling и тесты
Все команды выполняются из корня проекта.
- mypy:
```commandline
mypy .
```
- flake8:
```commandline
flake8
```
- тесты (в текущей реализации проходят при запущенном redis):
```commandline
pytest tests/ 
```
Остановить контейнер с redis:
```commandline
sudo docker-compose down
```
## Сборка и запуск проекта в контейнерах (выполнение команды из корня проекта)
```commandline
sudo docker-compose up -d
```
- Работа с api-методами:

В браузере перейдите по ссылке `http://127.0.0.1:8000/docs`

О получении информации о логировании и кэшировании - см. "Запуск проекта локально".

Остановить контейнеры с удалением сохранённых данных:
```commandline
sudo docker-compose down -v
```

### Замечания по реализации задания:
см. [файл](issues.md) 
