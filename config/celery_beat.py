from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-habit-reminders': {
        'task': 'habits.tasks.send_habit_reminders',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
    'cleanup-old-habits': {
        'task': 'habits.tasks.cleanup_old_habits',
        'schedule': crontab(hour=2, minute=0),  # Каждый день в 2:00
    },
}