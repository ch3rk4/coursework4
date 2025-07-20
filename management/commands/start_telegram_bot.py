from django.core.management.base import BaseCommand

from telegram_bot.bot import setup_bot


class Command(BaseCommand):
    """Команда для запуска Telegram бота."""

    help = "Запуск Telegram бота"

    def handle(self, *args, **options):
        self.stdout.write("Запуск Telegram бота...")
        app = setup_bot()
        app.run_polling()
