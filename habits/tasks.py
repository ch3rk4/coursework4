from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Habit
from telegram_bot.services import TelegramService


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках."""
    current_time = timezone.now().time()
    current_date = timezone.now().date()

    # Получаем привычки, которые должны выполняться в текущее время
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__telegram_user__is_active=True
    )

    telegram_service = TelegramService()

    for habit in habits:
        # Проверяем периодичность
        if should_send_reminder(habit, current_date):
            habit_text = f"Я буду {habit.action} в {habit.time} в {habit.place}"
            telegram_service.send_habit_reminder(habit.user.id, habit_text)


def should_send_reminder(habit, current_date):
    """Проверка, нужно ли отправлять напоминание с учетом периодичности."""
    if habit.periodicity == 1:  # Ежедневно
        return True

    # Для других периодичностей можно добавить логику
    # основанную на дате последнего выполнения
    return True


@shared_task
def cleanup_old_habits():
    """Очистка старых привычек."""
    old_date = timezone.now() - timedelta(days=365)
    deleted_count = Habit.objects.filter(created_at__lt=old_date).count()
    Habit.objects.filter(created_at__lt=old_date).delete()
    return f"Удалено {deleted_count} старых привычек"