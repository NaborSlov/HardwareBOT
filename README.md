# Django + Telegram Bot для управления промышленным оборудованием

Проект представляет собой Django-приложение с интегрированным Telegram-ботом для управления промышленным оборудованием. Использует FSM (Finite State Machine) для диалогов с пользователями.

## Структура проекта

```
/workspace/
├── Dockerfile              # Docker образ для приложения
├── docker-compose.yml      # Оркестрация сервисов (backend, bot, migrate, db)
├── requirements.txt        # Зависимости Python
├── manage.py               # Django management script
├── root/                   # Основной Django проект
│   ├── settings.py         # Настройки проекта
│   ├── urls.py             # Корневые URL
│   └── wsgi.py             # WSGI конфигурация
├── machinery/              # Приложение для управления оборудованием
│   ├── models.py           # Модели оборудования
│   ├── views.py            # Представления API
│   └── admin.py            # Django admin конфигурация
└── tg_bot/                 # Telegram бот
    ├── main_bot.py         # Основная логика бота
    ├── models.py           # Модели бота
    ├── forms.py            # Формы для FSM
    ├── management/
    │   └── commands/
    │       └── runbot.py   # Команда для запуска бота
    └── store/
        ├── handlers/       # Обработчики сообщений бота
        └── utils/          # Утилиты
```

## Требования

- Docker и Docker Compose
- Или локально: Python 3.10+, pip

## Быстрый старт с Docker

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Создание файла окружения

Создайте файл `.env` в корне проекта на основе примера:

```bash
cp env-ci .env
```

Отредактируйте `.env` и заполните реальными значениями:

```env
# Django настройки
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Telegram Bot
API_TOKEN=your-telegram-bot-token
PER_PAGE=10

# PostgreSQL настройки
POSTGRES_HOST=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_DB=machinery_db
```

**Важно:** 
- `SECRET_KEY` должен быть уникальной случайной строкой
- `API_TOKEN` получите у [@BotFather](https://t.me/BotFather) в Telegram
- В production установите `DEBUG=False`

### 3. Запуск через Docker Compose

```bash
# Запуск всех сервисов
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

Проект автоматически выполнит:
- Миграции базы данных
- Запуск Django сервера на порту 8000
- Запуск Telegram бота
- Запуск PostgreSQL

### 4. Проверка работы

- **Django админка:** http://localhost:8000/admin
- **API endpoint:** http://localhost:8000/api/
- **Telegram бот:** найдите вашего бота в Telegram и нажмите /start

### 5. Остановка сервисов

```bash
docker-compose down
```

## Локальная разработка (без Docker)

### 1. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка окружения

Создайте файл `.env` (см. раздел Docker выше).

### 4. Миграции базы данных

Для локальной разработки можно использовать SQLite или поднять PostgreSQL:

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запуск Django сервера

```bash
python manage.py runserver
```

### 7. Запуск Telegram бота (в отдельном терминале)

```bash
source venv/bin/activate  # Активируйте venv если нужно
python manage.py runbot
```

## Доступные команды

| Команда | Описание |
|---------|----------|
| `python manage.py runserver` | Запуск Django dev сервера |
| `python manage.py runbot` | Запуск Telegram бота |
| `python manage.py migrate` | Применение миграций БД |
| `python manage.py makemigrations` | Создание новых миграций |
| `python manage.py createsuperuser` | Создание администратора |
| `python manage.py test` | Запуск тестов |

## Архитектура

### Backend (Django)
- REST API для управления оборудованием
- Django Admin для администрирования
- ORM модели для хранения данных

### Telegram Bot
- FSM (Finite State Machine) для пошаговых диалогов
- Интеграция с Django моделями
- Обработка команд и состояний

### База данных
- PostgreSQL 15
- Автоматический healthcheck
- Персистентное хранилище через volume

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Секретный ключ Django | Обязательна |
| `DEBUG` | Режим отладки | `False` |
| `ALLOWED_HOSTS` | Разрешённые хосты | `localhost,127.0.0.1` |
| `API_TOKEN` | Токен Telegram бота | Обязательна |
| `PER_PAGE` | Количество элементов на страницу | `10` |
| `POSTGRES_HOST` | Хост PostgreSQL | `db` |
| `POSTGRES_USER` | Пользователь PostgreSQL | Обязательна |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | Обязательна |
| `POSTGRES_DB` | Имя базы данных | Обязательна |

## Troubleshooting

### Бот не запускается
- Проверьте правильность `API_TOKEN` в `.env`
- Убедитесь, что бот активирован в Telegram
- Проверьте логи: `docker-compose logs bot`

### Ошибки подключения к БД
- Убедитесь, что PostgreSQL запущен: `docker-compose ps`
- Проверьте переменные окружения в `.env`
- Дождитесь завершения healthcheck БД

### Миграции не применяются
- Очистите кэш миграций и примените заново:
  ```bash
  docker-compose run backend python manage.py migrate --run-syncdb
  ```

## Безопасность

⚠️ **Внимание:**
- Не коммитьте файл `.env` в репозиторий
- В production всегда устанавливайте `DEBUG=False`
- Используйте сложные пароли для PostgreSQL
- Регулярно обновляйте зависимости

## Лицензия

[Укажите лицензию вашего проекта]
