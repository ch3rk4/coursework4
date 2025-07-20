#!/bin/bash

# Скрипт для деплоя

echo "Начало деплоя..."

# Обновление кода
git pull origin main

# Остановка сервисов
docker-compose down

# Сборка образов
docker-compose build

# Запуск сервисов
docker-compose up -d

# Применение миграций
docker-compose exec -T web python manage.py migrate

# Сбор статических файлов
docker-compose exec -T web python manage.py collectstatic --noinput

# Проверка статуса
docker-compose ps

echo "Деплой завершен!"