from django.core.management.base import BaseCommand

from habits.models import Habit


class Command(BaseCommand):
    """Команда для проверки состояния привычек."""

    help = "Проверка состояния привычек в системе"

    def handle(self, *args, **options):
        total_habits = Habit.objects.count()
        public_habits = Habit.objects.filter(is_public=True).count()
        pleasant_habits = Habit.objects.filter(is_pleasant=True).count()

        self.stdout.write(f"Всего привычек: {total_habits}")
        self.stdout.write(f"Публичных привычек: {public_habits}")
        self.stdout.write(f"Приятных привычек: {pleasant_habits}")

        # Проверка привычек с проблемами валидации
        problematic_habits = []
        for habit in Habit.objects.all():
            try:
                habit.clean()
            except Exception as e:
                problematic_habits.append((habit.id, str(e)))

        if problematic_habits:
            self.stdout.write(
                self.style.WARNING("Найдены привычки с проблемами валидации:")
            )
            for habit_id, error in problematic_habits:
                self.stdout.write(f"ID {habit_id}: {error}")
        else:
            self.stdout.write(self.style.SUCCESS("Все привычки проходят валидацию!"))
