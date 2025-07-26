from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from habits.models import Habit
from telegram_bot.models import TelegramUser

User = get_user_model()


class Command(BaseCommand):
    """
    Команда для создания демонстрационных данных.

    Создает администратора, демо-пользователя и несколько примеров привычек
    для демонстрации возможностей системы.
    """

    help = "Создание демонстрационных данных для трекера привычек"

    def add_arguments(self, parser):
        """Добавление аргументов командной строки."""
        parser.add_argument(
            "--skip-admin",
            action="store_true",
            help="Пропустить создание администратора",
        )
        parser.add_argument(
            "--skip-demo-user",
            action="store_true",
            help="Пропустить создание демо-пользователя",
        )

    def handle(self, *args, **options):
        """Основная логика команды."""
        self.stdout.write("🚀 Начинаем создание демонстрационных данных...")

        with transaction.atomic():
            # Создание администратора
            if not options["skip_admin"]:
                admin_user = self._create_admin_user()

            # Создание демо-пользователя
            if not options["skip_demo_user"]:
                demo_user = self._create_demo_user()
                demo_telegram = self._create_demo_telegram_user(demo_user)
                self._create_demo_habits(demo_user)

        self.stdout.write(
            self.style.SUCCESS("✅ Демонстрационные данные успешно созданы!")
        )
        self._print_summary()

    def _create_admin_user(self):
        """Создание администратора."""
        admin_email = "admin@example.com"
        admin_password = "admin123"

        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(f"⚠️  Администратор с email {admin_email} уже существует")
            return User.objects.get(email=admin_email)

        admin_user = User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            first_name="Администратор",
            last_name="Системы",
        )

        self.stdout.write(self.style.SUCCESS(f"👑 Создан администратор: {admin_email}"))
        return admin_user

    def _create_demo_user(self):
        """Создание демонстрационного пользователя."""
        demo_email = "demo@example.com"
        demo_password = "demo123"

        if User.objects.filter(email=demo_email).exists():
            self.stdout.write(
                f"⚠️  Демо-пользователь с email {demo_email} уже существует"
            )
            return User.objects.get(email=demo_email)

        demo_user = User.objects.create_user(
            email=demo_email,
            password=demo_password,
            first_name="Демо",
            last_name="Пользователь",
        )

        self.stdout.write(
            self.style.SUCCESS(f"👤 Создан демо-пользователь: {demo_email}")
        )
        return demo_user

    def _create_demo_telegram_user(self, user):
        """Создание Telegram пользователя для демо."""
        chat_id = "123456789"

        if TelegramUser.objects.filter(user=user).exists():
            return TelegramUser.objects.get(user=user)

        telegram_user = TelegramUser.objects.create(user=user, telegram_chat_id=chat_id)

        self.stdout.write(
            self.style.SUCCESS(f"🤖 Создан Telegram пользователь с Chat ID: {chat_id}")
        )
        return telegram_user

    def _create_demo_habits(self, user):
        """Создание демонстрационных привычек."""
        habits_data = [
            {
                "place": "Кухня",
                "time": "08:00",
                "action": "Выпить стакан воды утром",
                "execution_time": 60,
                "periodicity": 1,
                "is_public": True,
                "reward": "Можно выпить кофе",
            },
            {
                "place": "Спортзал",
                "time": "18:00",
                "action": "Силовая тренировка",
                "execution_time": 90,
                "periodicity": 2,
                "is_public": True,
            },
            {
                "place": "Дом",
                "time": "22:00",
                "action": "Читать книгу перед сном",
                "execution_time": 120,
                "periodicity": 1,
                "is_public": False,
            },
            {
                "place": "Офис",
                "time": "12:00",
                "action": "Медитация",
                "execution_time": 300,  # 5 минут
                "periodicity": 1,
                "is_public": True,
            },
            {
                "place": "Кухня",
                "time": "09:00",
                "action": "Выпить чашку зеленого чая",
                "execution_time": 180,  # 3 минуты
                "periodicity": 1,
                "is_pleasant": True,  # Приятная привычка
                "is_public": True,
            },
        ]

        created_habits = []
        for habit_data in habits_data:
            habit, created = Habit.objects.get_or_create(
                user=user, action=habit_data["action"], defaults=habit_data
            )
            if created:
                created_habits.append(habit)
                self.stdout.write(f"✨ Создана привычка: {habit.action}")

        self.stdout.write(
            self.style.SUCCESS(f"📝 Создано {len(created_habits)} привычек")
        )

    def _print_summary(self):
        """Вывод итоговой информации."""
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 ИТОГОВАЯ ИНФОРМАЦИЯ")
        self.stdout.write("=" * 60)

        self.stdout.write("🔐 Учетные данные для входа:")
        self.stdout.write("   👑 Администратор:")
        self.stdout.write("      Email: admin@example.com")
        self.stdout.write("      Пароль: admin123")
        self.stdout.write("   👤 Демо-пользователь:")
        self.stdout.write("      Email: demo@example.com")
        self.stdout.write("      Пароль: demo123")

        self.stdout.write("\n🌐 Доступные URL:")
        self.stdout.write("   📖 API документация: /api/docs/")
        self.stdout.write("   🔧 Админ-панель: /admin/")
        self.stdout.write("   🏠 API корень: /api/")

        self.stdout.write("\n🤖 Telegram настройки:")
        self.stdout.write("   Chat ID для тестов: 123456789")
        self.stdout.write("   Подключение: POST /api/telegram/connect/")

        self.stdout.write("\n🎯 Статистика:")
        self.stdout.write(f"   Всего пользователей: {User.objects.count()}")
        self.stdout.write(f"   Всего привычек: {Habit.objects.count()}")
        self.stdout.write(
            f"   Публичных привычек: {Habit.objects.filter(is_public=True).count()}"
        )
        self.stdout.write("=" * 60)
