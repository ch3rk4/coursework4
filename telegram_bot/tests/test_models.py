from django.contrib.auth import get_user_model
from django.test import TestCase

from telegram_bot.models import TelegramUser

User = get_user_model()


class TelegramUserModelTest(TestCase):
    """Тесты модели TelegramUser."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_create_telegram_user(self):
        """Тест создания Telegram пользователя."""
        telegram_user = TelegramUser.objects.create(
            user=self.user, telegram_chat_id="123456789"
        )
        self.assertEqual(str(telegram_user), "testuser - 123456789")
        self.assertTrue(telegram_user.is_active)

    def test_unique_chat_id(self):
        """Тест уникальности chat_id."""
        TelegramUser.objects.create(user=self.user, telegram_chat_id="123456789")

        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpass123"
        )

        with self.assertRaises(Exception):  # IntegrityError
            TelegramUser.objects.create(user=other_user, telegram_chat_id="123456789")
