from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from habits.models import Habit
from habits.tasks import send_habit_reminders
from telegram_bot.models import TelegramUser

User = get_user_model()


class TasksTest(TestCase):
    """Тесты задач Celery."""

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
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00',
            action='Выпить воды',
            execution_time=60
        )

    @patch('habits.tasks.TelegramService')
    @patch('habits.tasks.timezone')
    def test_send_habit_reminders(self, mock_timezone, mock_telegram_service):
        """Тест отправки напоминаний."""
        # Настройка мока времени
        mock_time = MagicMock()
        mock_time.hour = 8
        mock_time.minute = 0
        mock_timezone.now.return_value.time.return_value = mock_time
        mock_timezone.now.return_value.date.return_value = MagicMock()

        # Настройка мока сервиса
        mock_service_instance = MagicMock()
        mock_telegram_service.return_value = mock_service_instance
        mock_service_instance.send_habit_reminder.return_value = True

        # Выполнение задачи
        send_habit_reminders()

        # Проверка вызова
        mock_service_instance.send_habit_reminder.assert_called_once()

