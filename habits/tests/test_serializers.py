from django.contrib.auth import get_user_model
from django.test import TestCase

from habits.serializers import HabitSerializer

User = get_user_model()


class HabitSerializerTest(TestCase):
    """Тесты сериализатора привычек."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_valid_habit_serializer(self):
        """Тест валидного сериализатора."""
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Выпить воды",
            "execution_time": 60,
            "periodicity": 1,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_execution_time(self):
        """Тест невалидного времени выполнения."""
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Медитация",
            "execution_time": 150,  # Больше 120
            "periodicity": 1,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("execution_time", str(serializer.errors))

    def test_pleasant_habit_with_reward(self):
        """Тест приятной привычки с наградой."""
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Выпить чай",
            "execution_time": 60,
            "is_pleasant": True,
            "reward": "Печенье",
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
