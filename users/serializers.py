from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Сериализатор для создания пользователя через email.

    Поскольку мы убрали username из модели, создание происходит только через email.
    """

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "telegram_chat_id",
        )

    def validate_email(self, value):
        """Дополнительная валидация email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return value.lower()  # Приводим к нижнему регистру


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения информации о пользователе.

    Включает поле display_name для удобного отображения имени.
    """

    display_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "telegram_chat_id",
            "date_joined",
            "is_active",
        )
        read_only_fields = ("id", "date_joined", "is_active")

    def validate_email(self, value):
        """Валидация email при обновлении."""
        # Проверяем уникальность только если email изменился
        if self.instance and self.instance.email != value:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "Пользователь с таким email уже существует."
                )
        return value.lower()


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Отдельный сериализатор для обновления профиля пользователя.

    Исключает поля, которые не должны изменяться через API.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "telegram_chat_id")

    def validate_telegram_chat_id(self, value):
        """Валидация Telegram Chat ID."""
        if value and not value.isdigit():
            raise serializers.ValidationError(
                "Telegram Chat ID должен содержать только цифры."
            )
        return value
