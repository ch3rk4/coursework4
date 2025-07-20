from rest_framework import serializers
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Telegram пользователя."""

    class Meta:
        model = TelegramUser
        fields = ['telegram_chat_id', 'is_active', 'created_at']
        read_only_fields = ['created_at']