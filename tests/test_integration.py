from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from habits.models import Habit
from telegram_bot.models import TelegramUser

User = get_user_model()


class HabitWorkflowIntegrationTest(TestCase):
    """Интеграционные тесты workflow привычек."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_complete_habit_workflow(self):
        """Тест полного workflow работы с привычками."""
        # 1. Создание привычки
        habit_data = {
            'place': 'Спортзал',
            'time': '07:00',
            'action': 'Тренировка',
            'execution_time': 90,
            'periodicity': 1,
            'is_public': True
        }

        create_url = reverse('habits:habit-list-create')
        response = self.client.post(create_url, habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        habit_id = response.data['id']

        # 2. Получение списка привычек
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 3. Обновление привычки
        update_data = {'place': 'Дом'}
        detail_url = reverse('habits:habit-detail', kwargs={'pk': habit_id})
        response = self.client.patch(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'Дом')

        # 4. Проверка публичных привычек
        public_url = reverse('habits:public-habits')
        response = self.client.get(public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # 5. Удаление привычки
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 6. Проверка что привычка удалена
        response = self.client.get(create_url)
        self.assertEqual(len(response.data['results']), 0)

    def test_telegram_integration_workflow(self):
        """Тест workflow интеграции с Telegram."""
        # 1. Подключение Telegram
        connect_url = reverse('telegram_bot:connect-telegram')
        data = {'chat_id': '123456789'}
        response = self.client.post(connect_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Проверка создания TelegramUser
        self.assertTrue(
            TelegramUser.objects.filter(
                user=self.user,
                telegram_chat_id='123456789'
            ).exists()
        )

        # 3. Отключение Telegram
        disconnect_url = reverse('telegram_bot:disconnect-telegram')
        response = self.client.post(disconnect_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 4. Проверка деактивации
        telegram_user = TelegramUser.objects.get(user=self.user)
        self.assertFalse(telegram_user.is_active)


class AuthenticationWorkflowTest(TestCase):
    """Тесты workflow аутентификации."""

    def setUp(self):
        self.client = APIClient()

    def test_registration_and_authentication_workflow(self):
        """Тест регистрации и аутентификации."""
        # 1. Регистрация
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }

        register_url = reverse('user-list')  # djoser endpoint
        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. Получение JWT токена
        login_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }

        login_url = reverse('jwt-create')  # djoser JWT endpoint
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

        # 3. Использование токена для доступа к API
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        habits_url = reverse('habits:habit-list-create')
        response = self.client.get(habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
