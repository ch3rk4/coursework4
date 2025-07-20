# 🎯 Трекер полезных привычек

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red?style=flat-square&logo=redis)](https://redis.io/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square&logo=telegram)](https://telegram.org/)

Веб-приложение для отслеживания и формирования полезных привычек с интеграцией Telegram бота для напоминаний. Основано на принципах из книги Джеймса Клира "Атомные привычки".

## 📖 Содержание

- [Возможности](#-возможности)
- [Технологии](#-технологии)
- [Быстрый старт](#-быстрый-старт)
- [Установка](#-установка)
- [API документация](#-api-документация)
- [Telegram бот](#-telegram-бот)
- [Тестирование](#-тестирование)
- [Развертывание](#-развертывание)
- [Структура проекта](#-структура-проекта)
- [Вклад в проект](#-вклад-в-проект)

## ✨ Возможности

### 🎯 Управление привычками
- ✅ Создание и редактирование привычек
- ✅ Полезные и приятные привычки
- ✅ Связанные привычки и система вознаграждений
- ✅ Настройка периодичности выполнения
- ✅ Публичные привычки для вдохновения

### 🔔 Уведомления
- ✅ Telegram бот для напоминаний
- ✅ Автоматические уведомления по расписанию
- ✅ Персонализированные сообщения

### 🛡️ Безопасность и права доступа
- ✅ JWT аутентификация
- ✅ Личные привычки (CRUD для владельца)
- ✅ Просмотр публичных привычек
- ✅ Валидация данных

### 🔧 Дополнительно
- ✅ REST API с пагинацией
- ✅ Админ-панель Django
- ✅ Docker контейнеризация
- ✅ CI/CD с GitHub Actions
- ✅ Покрытие тестами 80%+

## 🛠️ Технологии

### Backend
- **Python 3.11+** - язык программирования
- **Django 4.2** - веб-фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - основная база данных
- **Redis** - кэш и брокер сообщений
- **Celery** - асинхронные задачи

### Интеграции
- **python-telegram-bot** - Telegram API
- **JWT** - аутентификация
- **CORS** - поддержка фронтенда

### DevOps
- **Docker & Docker Compose** - контейнеризация
- **GitHub Actions** - CI/CD
- **Nginx** - веб-сервер (продакшн)
- **Gunicorn** - WSGI сервер

### Тестирование
- **pytest** - тестовый фреймворк
- **coverage** - покрытие кода
- **flake8** - линтер

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.11+
- Docker и Docker Compose
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/habits-tracker.git
cd habits-tracker
```

### 2. Запуск через Docker (рекомендуется)

```bash
# Создание .env файла
cp .env.example .env
# Отредактируйте .env файл с вашими настройками

# Сборка и запуск
docker-compose up -d --build

# Применение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic --noinput
```

### 3. Доступ к приложению

- **API**: http://localhost:8000/api/
- **Админка**: http://localhost:8000/admin/
- **Документация API**: http://localhost:8000/api/docs/ (если настроена)

## 📦 Установка

### Локальная разработка

<details>
<summary>Развернуть инструкции для локальной установки</summary>

#### 1. Создание виртуального окружения

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 3. Настройка переменных окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` файл:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
POSTGRES_DB=habits_db
POSTGRES_USER=habits_user
POSTGRES_PASSWORD=habits_password
DB_HOST=localhost
REDIS_URL=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 4. Запуск служб

```bash
# Запуск PostgreSQL и Redis (через Docker)
docker run -d --name postgres -e POSTGRES_DB=habits_db -e POSTGRES_USER=habits_user -e POSTGRES_PASSWORD=habits_password -p 5432:5432 postgres:15
docker run -d --name redis -p 6379:6379 redis:7

# Или установите локально
```

#### 5. Применение миграций

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

#### 6. Запуск разработческих серверов

```bash
# Терминал 1: Django
python manage.py runserver

# Терминал 2: Celery Worker
celery -A config worker --loglevel=info

# Терминал 3: Celery Beat
celery -A config beat --loglevel=info
```

</details>

## 📚 API документация

### Аутентификация

```bash
# Регистрация
POST /api/auth/users/
{
  "username": "user",
  "email": "user@example.com",
  "password": "password123"
}

# Получение токена
POST /api/auth/jwt/create/
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Привычки

```bash
# Список привычек пользователя
GET /api/habits/
Authorization: Bearer <token>

# Создание привычки
POST /api/habits/
Authorization: Bearer <token>
{
  "place": "Дом",
  "time": "08:00",
  "action": "Выпить стакан воды",
  "execution_time": 60,
  "periodicity": 1,
  "is_public": false
}

# Редактирование привычки
PUT /api/habits/{id}/
PATCH /api/habits/{id}/

# Удаление привычки
DELETE /api/habits/{id}/

# Публичные привычки
GET /api/habits/public/
```

### Telegram интеграция

```bash
# Подключение Telegram
POST /api/telegram/connect/
Authorization: Bearer <token>
{
  "chat_id": "123456789"
}

# Отключение Telegram
POST /api/telegram/disconnect/
Authorization: Bearer <token>
```

### Пагинация

Все списки поддерживают пагинацию:

```bash
GET /api/habits/?page=1&page_size=5
```

## 🤖 Telegram бот

### Настройка бота

1. **Создайте бота через @BotFather:**
   - Отправьте `/start` боту @BotFather
   - Отправьте `/newbot`
   - Введите имя: `Habits Tracker Bot`
   - Введите username: `habits_tracker_bot`
   - Скопируйте полученный токен

2. **Добавьте токен в .env:**
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```

3. **Получите Chat ID:**
   - Отправьте `/start` вашему боту
   - Скопируйте Chat ID из ответа

4. **Подключите аккаунт:**
   ```bash
   POST /api/telegram/connect/
   {
     "chat_id": "your-chat-id"
   }
   ```

### Команды бота

- `/start` - Получить Chat ID
- `/help` - Справка по командам
- `/status` - Проверить статус подключения

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=. --cov-report=html --cov-report=term-missing

# Конкретное приложение
pytest habits/tests/

# Линтер
flake8 .
```

### Создание тестовых данных

```bash
python manage.py create_test_data
```

### Проверка готовности проекта

```bash
python manage.py check_project_ready
```

## 🚢 Развертывание

### Docker (продакшн)

```bash
# Создание .env для продакшна
cp .env.example .env.prod
# Настройте продакшн переменные

# Запуск
docker-compose -f docker-compose.prod.yml up -d --build

# Миграции
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Сбор статики
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### CI/CD с GitHub Actions

1. **Настройте GitHub Secrets:**
   - `HOST` - IP сервера
   - `USERNAME` - пользователь сервера
   - `SSH_KEY` - приватный SSH ключ
   - `SECRET_KEY` - Django secret key
   - `POSTGRES_PASSWORD` - пароль БД
   - `TELEGRAM_BOT_TOKEN` - токен бота

2. **Автоматический деплой:**
   ```bash
   git push origin main
   ```

### Ручной деплой

<details>
<summary>Инструкции для ручного деплоя</summary>

#### На сервере Ubuntu/Debian:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Клонирование проекта
git clone https://github.com/yourusername/habits-tracker.git /opt/habits-tracker
cd /opt/habits-tracker

# Настройка .env
cp .env.example .env
nano .env

# Запуск
docker-compose -f docker-compose.prod.yml up -d --build
```

</details>

## 📂 Структура проекта

```
habits_tracker/
├── 📁 config/                 # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── 📁 habits/                 # Приложение привычек
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py              # Celery задачи
│   └── tests/
├── 📁 users/                 # Пользователи
│   ├── models.py
│   ├── serializers.py
│   └── tests/
├── 📁 telegram_bot/          # Telegram интеграция
│   ├── models.py
│   ├── services.py
│   ├── bot.py
│   └── tests/
├── 📁 docker/                # Docker файлы
├── 📁 .github/workflows/     # CI/CD
├── 📄 requirements.txt       # Python зависимости
├── 📄 docker-compose.yml     # Docker Compose
├── 📄 Dockerfile            # Docker образ
├── 📄 .env.example          # Пример переменных
└── 📄 README.md             # Этот файл
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Режим отладки | `True` |
| `POSTGRES_DB` | Имя базы данных | `habits_db` |
| `POSTGRES_USER` | Пользователь БД | `habits_user` |
| `POSTGRES_PASSWORD` | Пароль БД | - |
| `DB_HOST` | Хост БД | `localhost` |
| `REDIS_URL` | URL Redis | `redis://localhost:6379/0` |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | - |
| `ALLOWED_HOSTS` | Разрешенные хосты | `localhost,127.0.0.1` |

### Настройка Celery

Celery настроен для отправки напоминаний каждую минуту. Расписание можно изменить в `config/celery.py`:

```python
app.conf.beat_schedule = {
    'send-habit-reminders': {
        'task': 'habits.tasks.send_habit_reminders',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}
```

## ❓ Часто задаваемые вопросы

<details>
<summary>Как изменить периодичность напоминаний?</summary>

Отредактируйте файл `config/celery.py` и измените расписание в `beat_schedule`.

</details>

<details>
<summary>Как добавить новые поля в модель привычки?</summary>

1. Измените модель в `habits/models.py`
2. Создайте миграцию: `python manage.py makemigrations`
3. Примените миграцию: `python manage.py migrate`
4. Обновите сериализатор в `habits/serializers.py`

</details>

<details>
<summary>Как настроить SSL для продакшна?</summary>

Используйте Nginx с Let's Encrypt или CloudFlare для SSL терминации.

</details>

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! 

### Как внести вклад:

1. **Fork** репозитория
2. Создайте **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** изменения (`git commit -m 'Add amazing feature'`)
4. **Push** в branch (`git push origin feature/amazing-feature`)
5. Откройте **Pull Request**

### Правила разработки:

- Покрытие новых функций тестами
- Соответствие PEP 8 (проверка через flake8)
- Документирование API изменений
- Описательные commit сообщения

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 📞 Поддержка

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/habits-tracker/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/habits-tracker/discussions)
- 📧 **Email**: your.email@example.com

## 🏆 Благодарности

- [Джеймс Клир](https://jamesclear.com/) за книгу "Атомные привычки"
- Django и Django REST Framework сообществу
- Всем контрибьюторам проекта

---

<div align="center">

**[⬆ Наверх](#-трекер-полезных-привычек)**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>