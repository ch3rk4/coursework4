from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "password", "telegram_chat_id")


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "telegram_chat_id",
        )
        read_only_fields = ("id",)
