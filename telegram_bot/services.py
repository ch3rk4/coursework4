import logging
from telegram import Bot
from telegram.error import TelegramError
from django.conf import settings
from .models import TelegramUser

logger = logging.getLogger(__name__)


class TelegramService:
    """Сервис для работы с Telegram."""

    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    def send_message(self, chat_id: str, message: str) -> bool:
        """Отправка сообщения в Telegram."""
        try:
            self.bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"Сообщение отправлено в чат {chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"Ошибка отправки сообщения в чат {chat_id}: {e}")
            return False

    def send_habit_reminder(self, user_id: int, habit_text: str) -> bool:
        """Отправка напоминания о привычке."""
        try:
            telegram_user = TelegramUser.objects.get(user_id=user_id, is_active=True)
            message = f"🔔 Напоминание о привычке:\n\n{habit_text}"
            return self.send_message(telegram_user.telegram_chat_id, message)
        except TelegramUser.DoesNotExist:
            logger.warning(f"Telegram пользователь с user_id {user_id} не найден")
            return False