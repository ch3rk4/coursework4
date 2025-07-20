# scripts/setup_server.sh
#!/bin/bash

# Скрипт для первоначальной настройки Yandex Cloud сервера

echo "🚀 Настройка сервера для Habits Tracker..."

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Установка Git
sudo apt install -y git

# Создание директории для проекта
sudo mkdir -p /opt/habits_tracker
sudo chown $USER:$USER /opt/habits_tracker

# Клонирование проекта
cd /opt/habits_tracker
git clone https://github.com/yourusername/habits-tracker.git .

# Создание .env файла (заполните вручную)
cp .env.example .env
echo "⚠️  Не забудьте отредактировать файл .env с правильными настройками!"

# Настройка firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "✅ Базовая настройка сервера завершена!"
echo "Теперь отредактируйте .env файл и запустите:"
echo "docker-compose -f docker-compose.prod.yml up -d --build"