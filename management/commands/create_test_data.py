from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from habits.models import Habit
from telegram_bot.models import TelegramUser

User = get_user_model()


class Command(BaseCommand):
    """Команда для создания тестовых данных."""

    help = "Создание тестовых данных для разработки"

    def handle(self, *args, **options):
        # Создание тестовых пользователей
        user1, created = User.objects.get_or_create(
            username="test_user_1",
            defaults={
                "email": "user1@example.com",
                "first_name": "Тест",
                "last_name": "Пользователь 1",
            },
        )
        if created:
            user1.set_password("password123")
            user1.save()
            self.stdout.write(f"Создан пользователь: {user1.username}")

        user2, created = User.objects.get_or_create(
            username="test_user_2",
            defaults={
                "email": "user2@example.com",
                "first_name": "Тест",
                "last_name": "Пользователь 2",
            },
        )
        if created:
            user2.set_password("password123")
            user2.save()
            self.stdout.write(f"Создан пользователь: {user2.username}")

        # Создание тестовых привычек
        habits_data = [
            {
                "user": user1,
                "place": "Дом",
                "time": "08:00",
                "action": "Выпить стакан воды",
                "execution_time": 60,
                "is_public": True,
            },
            {
                "user": user1,
                "place": "Спортзал",
                "time": "18:00",
                "action": "Тренировка",
                "execution_time": 120,
                "reward": "Протеиновый коктейль",
            },
            {
                "user": user1,
                "place": "Кухня",
                "time": "09:00",
                "action": "Выпить кофе",
                "execution_time": 30,
                "is_pleasant": True,
            },
            {
                "user": user2,
                "place": "Парк",
                "time": "07:00",
                "action": "Утренняя пробежка",
                "execution_time": 120,
                "is_public": True,
                "periodicity": 2,
            },
        ]

        for habit_data in habits_data:
            habit, created = Habit.objects.get_or_create(
                user=habit_data["user"],
                action=habit_data["action"],
                defaults=habit_data,
            )
            if created:
                self.stdout.write(f"Создана привычка: {habit.action}")

        # Создание Telegram пользователей
        telegram_users_data = [
            {"user": user1, "telegram_chat_id": "123456789"},
            {"user": user2, "telegram_chat_id": "987654321"},
        ]

        for tg_data in telegram_users_data:
            tg_user, created = TelegramUser.objects.get_or_create(
                user=tg_data["user"], defaults=tg_data
            )
            if created:
                self.stdout.write(f"Создан Telegram пользователь: {tg_user}")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
