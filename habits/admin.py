from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Админка для привычек."""

    list_display = (
        'action', 'user', 'place', 'time',
        'is_pleasant', 'is_public', 'created_at'
    )
    list_filter = ('is_pleasant', 'is_public', 'created_at')
    search_fields = ('action', 'place', 'user__username')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Настройки', {
            'fields': ('is_pleasant', 'is_public', 'periodicity', 'execution_time')
        }),
        ('Связи и награды', {
            'fields': ('related_habit', 'reward')
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )