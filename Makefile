.PHONY: help install migrate test lint run docker-build docker-up docker-down

help:  ## Показать справку
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install:  ## Установить зависимости
	pip install -r requirements.txt

migrate:  ## Применить миграции
	python manage.py migrate

test:  ## Запустить тесты
	pytest --cov=. --cov-report=term-missing

lint:  ## Проверить код линтером
	flake8 .

run:  ## Запустить сервер разработки
	python manage.py runserver

docker-build:  ## Собрать Docker образы
	docker-compose build

docker-up:  ## Запустить Docker контейнеры
	docker-compose up -d

docker-down:  ## Остановить Docker контейнеры
	docker-compose down

docker-logs:  ## Просмотр логов Docker
	docker-compose logs -f

celery-worker:  ## Запустить Celery worker
	celery -A config worker --loglevel=info

celery-beat:  ## Запустить Celery beat
	celery -A config beat --loglevel=info

collectstatic:  ## Собрать статические файлы
	python manage.py collectstatic --noinput

superuser:  ## Создать суперпользователя
	python manage.py createsuperuser