"""Telegram бот для напоминаний."""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .models import TelegramUser

logger = logging.getLogger(__name__)
User = get_user_model()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    chat_id = str(update.effective_chat.id)

    await update.message.reply_text(
        f"Привет! Твой Chat ID: {chat_id}\n"
        f"Используй этот ID для подключения аккаунта в приложении трекера привычек."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    help_text = """
Доступные команды:
/start - Получить Chat ID для подключения
/help - Показать это сообщение
/status - Проверить статус подключения

Для подключения к аккаунту:
1. Скопируй Chat ID из сообщения /start
2. Перейди в настройки аккаунта в приложении
3. Добавь Chat ID в настройки Telegram
"""
    await update.message.reply_text(help_text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Проверка статуса подключения."""
    chat_id = str(update.effective_chat.id)

    try:
        telegram_user = TelegramUser.objects.get(
            telegram_chat_id=chat_id, is_active=True
        )
        await update.message.reply_text(
            f"✅ Аккаунт подключен к пользователю: {telegram_user.user.username}"
        )
    except TelegramUser.DoesNotExist:
        await update.message.reply_text(
            "❌ Аккаунт не подключен. Используй /start для получения Chat ID."
        )


def setup_bot():
    """Настройка бота."""
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))

    return application


if __name__ == "__main__":
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    app = setup_bot()
    app.run_polling()
