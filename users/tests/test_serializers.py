from django.test import TestCase
from django.contrib.auth import get_user_model
from users.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    """Тесты сериализаторов пользователей."""

    def test_user_create_serializer(self):
        """Тест сериализатора создания пользователя."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'telegram_chat_id': '123456789'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.telegram_chat_id, '123456789')

    def test_user_serializer(self):
        """Тест сериализатора пользователя."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        serializer = UserSerializer(user)
        expected_fields = {
            'id', 'email', 'username', 'first_name', 'last_name', 'telegram_chat_id'
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)
