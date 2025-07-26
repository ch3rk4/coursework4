from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с email как основным полем для входа."""

    # Явно убираем username как обязательное поле
    username = None

    # Email как основное поле для аутентификации
    email = models.EmailField(unique=True, verbose_name="Email")

    # Дополнительные поля
    telegram_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram Chat ID"
    )

    # Настройки аутентификации
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Строковое представление пользователя."""
        return self.email

    @property
    def display_name(self):
        """Возвращает отображаемое имя пользователя."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.email.split("@")[0]
