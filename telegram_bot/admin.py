from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Админка для Telegram пользователей."""

    list_display = ["user", "telegram_chat_id", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["user__username", "user__email", "telegram_chat_id"]
    readonly_fields = ["created_at"]
