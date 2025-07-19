from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    """Модель привычки."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )
    execution_time = models.PositiveIntegerField(
        verbose_name='Время на выполнение (секунды)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    def clean(self):
        """Валидация модели."""
        errors = {}

        # Проверка одновременного заполнения связанной привычки и вознаграждения
        if self.related_habit and self.reward:
            errors['related_habit'] = 'Нельзя указывать одновременно связанную привычку и вознаграждение.'
            errors['reward'] = 'Нельзя указывать одновременно связанную привычку и вознаграждение.'

        # Проверка времени выполнения
        if self.execution_time and self.execution_time > 120:
            errors['execution_time'] = 'Время выполнения не должно превышать 120 секунд.'

        # Проверка связанной привычки
        if self.related_habit and not self.related_habit.is_pleasant:
            errors['related_habit'] = 'В связанные привычки могут попадать только приятные привычки.'

        # Проверка приятной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            errors['is_pleasant'] = 'У приятной привычки не может быть вознаграждения или связанной привычки.'

        # Проверка периодичности
        if self.periodicity and self.periodicity > 7:
            errors['periodicity'] = 'Нельзя выполнять привычку реже, чем 1 раз в 7 дней.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)