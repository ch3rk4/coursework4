from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


class HabitAPITest(TestCase):
    """Тесты API привычек."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест создания привычки через API."""
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Спортзал",
            "time": "07:00",
            "action": "Тренировка",
            "execution_time": 90,
            "periodicity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().user, self.user)

    def test_list_habits(self):
        """Тест получения списка привычек."""
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Зарядка",
            execution_time=60,
        )

        url = reverse("habits:habit-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_public_habits_list(self):
        """Тест получения списка публичных привычек."""
        # Создаем публичную привычку
        Habit.objects.create(
            user=self.user,
            place="Парк",
            time="06:00",
            action="Пробежка",
            execution_time=120,
            is_public=True,
        )

        # Создаем приватную привычку
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Медитация",
            execution_time=60,
            is_public=False,
        )

        url = reverse("habits:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Только публичная

    def test_habit_permissions(self):
        """Тест прав доступа к привычкам."""
        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpass123"
        )

        habit = Habit.objects.create(
            user=other_user,
            place="Офис",
            time="09:00",
            action="Планирование дня",
            execution_time=30,
        )

        url = reverse("habits:habit-detail", kwargs={"pk": habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
