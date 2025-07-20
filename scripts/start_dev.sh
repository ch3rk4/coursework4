#!/bin/bash

# Скрипт для запуска разработки

echo "Запуск разработческого окружения..."

# Активация виртуального окружения
source venv/bin/activate

# Применение миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск сервера в фоне
python manage.py runserver &
SERVER_PID=$!

# Запуск Celery worker в фоне
celery -A config worker --loglevel=info &
WORKER_PID=$!

# Запуск Celery beat в фоне
celery -A config beat --loglevel=info &
BEAT_PID=$!

echo "Сервисы запущены:"
echo "Django server PID: $SERVER_PID"
echo "Celery worker PID: $WORKER_PID"
echo "Celery beat PID: $BEAT_PID"

# Функция для остановки всех процессов
cleanup() {
    echo "Остановка сервисов..."
    kill $SERVER_PID $WORKER_PID $BEAT_PID 2>/dev/null
    exit 0
}

# Обработка сигнала завершения
trap cleanup SIGINT SIGTERM

# Ожидание
wait