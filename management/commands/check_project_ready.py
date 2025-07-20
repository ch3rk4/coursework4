from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    """Команда для проверки готовности проекта к деплою."""

    help = 'Проверка готовности проекта к деплою'

    def handle(self, *args, **options):
        checks = []

        # Проверка переменных окружения
        required_env_vars = [
            'SECRET_KEY', 'DATABASE_URL', 'REDIS_URL', 'TELEGRAM_BOT_TOKEN'
        ]

        for var in required_env_vars:
            if os.getenv(var):
                checks.append(f'✅ {var} - настроена')
            else:
                checks.append(f'❌ {var} - НЕ настроена')

        # Проверка файлов
        required_files = [
            'requirements.txt',
            'Dockerfile',
            'docker-compose.yml',
            '.github/workflows/main.yml',
            'nginx.conf'
        ]

        for file in required_files:
            if os.path.exists(file):
                checks.append(f'✅ {file} - существует')
            else:
                checks.append(f'❌ {file} - НЕ существует')

        # Проверка приложений
        required_apps = ['habits', 'users', 'telegram_bot']
        installed_apps = [app.split('.')[-1] for app in settings.INSTALLED_APPS]

        for app in required_apps:
            if app in installed_apps:
                checks.append(f'✅ Приложение {app} - установлено')
            else:
                checks.append(f'❌ Приложение {app} - НЕ установлено')

        # Вывод результатов
        self.stdout.write('Проверка готовности проекта:')
        self.stdout.write('-' * 40)

        for check in checks:
            if '✅' in check:
                self.stdout.write(self.style.SUCCESS(check))
            else:
                self.stdout.write(self.style.ERROR(check))

        success_count = len([c for c in checks if '✅' in c])
        total_count = len(checks)

        self.stdout.write('-' * 40)
        self.stdout.write(f'Результат: {success_count}/{total_count} проверок пройдено')

        if success_count == total_count:
            self.stdout.write(
                self.style.SUCCESS('🎉 Проект готов к деплою!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Есть проблемы, которые нужно исправить')
            )