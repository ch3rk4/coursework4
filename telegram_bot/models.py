from django.db import models
from django.conf import settings


class TelegramUser(models.Model):
    """Модель пользователя Telegram."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    telegram_chat_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Telegram Chat ID'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'

    def __str__(self):
        return f'{self.user.username} - {self.telegram_chat_id}'