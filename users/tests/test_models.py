from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты модели User."""

    def test_create_user(self):
        """Тест создания пользователя."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_superuser(self):
        """Тест создания суперпользователя."""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_email_unique(self):
        """Тест уникальности email."""
        User.objects.create_user(
            username='user1',
            email='test@example.com',
            password='pass123'
        )

        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create_user(
                username='user2',
                email='test@example.com',
                password='pass123'
            )