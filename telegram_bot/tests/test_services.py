from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from telegram_bot.services import TelegramService
from telegram_bot.models import TelegramUser

User = get_user_model()


class TelegramServiceTest(TestCase):
    """Тесты сервиса Telegram."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.telegram_user = TelegramUser.objects.create(
            user=self.user,
            telegram_chat_id='123456789'
        )

    @patch('telegram_bot.services.Bot')
    def test_send_message_success(self, mock_bot):
        """Тест успешной отправки сообщения."""
        mock_bot_instance = MagicMock()
        mock_bot.return_value = mock_bot_instance
        mock_bot_instance.send_message.return_value = True

        service = TelegramService()
        result = service.send_message('123456789', 'Test message')

        self.assertTrue(result)
        mock_bot_instance.send_message.assert_called_once_with(
            chat_id='123456789',
            text='Test message'
        )

    @patch('telegram_bot.services.Bot')
    def test_send_habit_reminder(self, mock_bot):
        """Тест отправки напоминания о привычке."""
        mock_bot_instance = MagicMock()
        mock_bot.return_value = mock_bot_instance
        mock_bot_instance.send_message.return_value = True

        service = TelegramService()
        result = service.send_habit_reminder(self.user.id, 'Выпить воды')

        self.assertTrue(result)
        mock_bot_instance.send_message.assert_called_once()

