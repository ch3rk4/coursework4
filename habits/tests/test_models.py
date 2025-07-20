from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты модели Habit."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_habit(self):
        """Тест создания привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00',
            action='Выпить стакан воды',
            execution_time=60,
            periodicity=1
        )
        self.assertEqual(str(habit), 'Выпить стакан воды в 08:00:00 в Дом')

    def test_habit_validation_execution_time(self):
        """Тест валидации времени выполнения."""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00',
            action='Медитация',
            execution_time=150,  # Больше 120 секунд
            periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_habit_validation_reward_and_related_habit(self):
        """Тест валидации одновременного указания награды и связанной привычки."""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00',
            action='Выпить чай',
            execution_time=60,
            is_pleasant=True
        )

        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00',
            action='Зарядка',
            execution_time=60,
            reward='Шоколадка',
            related_habit=pleasant_habit
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_habit_validation_periodicity(self):
        """Тест валидации периодичности."""
        habit = Habit(
            user=self.user,
            place='Дом',
            time='08:00',
            action='Читать',
            execution_time=60,
            periodicity=10  # Больше 7 дней
        )
        with self.assertRaises(ValidationError):
            habit.clean()