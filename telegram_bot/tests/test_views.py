from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from telegram_bot.models import TelegramUser

User = get_user_model()


class TelegramViewsTest(TestCase):
    """Тесты представлений Telegram."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_connect_telegram(self):
        """Тест подключения Telegram."""
        url = reverse("telegram_bot:connect-telegram")
        data = {"chat_id": "123456789"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            TelegramUser.objects.filter(
                user=self.user, telegram_chat_id="123456789"
            ).exists()
        )

    def test_connect_telegram_without_chat_id(self):
        """Тест подключения без chat_id."""
        url = reverse("telegram_bot:connect-telegram")
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("chat_id is required", response.data["error"])

    def test_disconnect_telegram(self):
        """Тест отключения Telegram."""
        telegram_user = TelegramUser.objects.create(
            user=self.user, telegram_chat_id="123456789"
        )

        url = reverse("telegram_bot:disconnect-telegram")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        telegram_user.refresh_from_db()
        self.assertFalse(telegram_user.is_active)
