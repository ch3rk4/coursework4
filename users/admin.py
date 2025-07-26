from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя в админке.

    Поскольку мы убрали username, создание пользователя происходит только через email.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)  # Только email для создания

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле username из формы, если оно есть
        if 'username' in self.fields:
            del self.fields['username']


class CustomUserChangeForm(UserChangeForm):
    """
    Форма для изменения существующего пользователя в админке.

    Включает все поля, которые администратор может изменять.
    """

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "telegram_chat_id", "is_active", "is_staff")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле username из формы, если оно есть
        if 'username' in self.fields:
            del self.fields['username']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Административный интерфейс для кастомной модели пользователя.

    Полностью адаптирован под нашу модель без поля username.
    """

    # Используем наши кастомные формы
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Поля для отображения в списке пользователей
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "date_joined"]

    # Поля для фильтрации в правой панели
    list_filter = ["is_active", "is_staff", "is_superuser", "date_joined"]

    # Поля для поиска
    search_fields = ["email", "first_name", "last_name"]

    # Сортировка по умолчанию (заменяем username на email)
    ordering = ["email"]

    # Фильтр по дате - показываем пользователей по дням
    date_hierarchy = "date_joined"

    # Настройка полей в форме редактирования пользователя
    fieldsets = (
        # Основная информация
        ("Основная информация", {
            "fields": ("email", "password")
        }),

        # Персональная информация
        ("Персональная информация", {
            "fields": ("first_name", "last_name")
        }),

        # Telegram интеграция
        ("Telegram", {
            "fields": ("telegram_chat_id",),
            "classes": ("collapse",),  # Сворачиваемая секция
            "description": "Настройки интеграции с Telegram ботом"
        }),

        # Права доступа
        ("Права доступа", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),

        # Важные даты
        ("Важные даты", {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",),
        }),
    )

    # Настройка полей для формы добавления нового пользователя
    add_fieldsets = (
        ("Создание пользователя", {
            "classes": ("wide",),  # Широкая форма
            "fields": ("email", "password1", "password2"),
            "description": "Введите email и пароль для нового пользователя"
        }),
        ("Дополнительная информация", {
            "classes": ("wide", "collapse"),
            "fields": ("first_name", "last_name", "telegram_chat_id"),
        }),
    )

    # Поля только для чтения
    readonly_fields = ["date_joined", "last_login"]

    # Количество пользователей на странице
    list_per_page = 25

    # Максимальное количество элементов для показа опции "Выбрать все"
    list_max_show_all = 200

    def get_readonly_fields(self, request, obj=None):
        """
        Определяет поля только для чтения в зависимости от прав пользователя.

        Суперпользователь может редактировать все, обычные админы - ограниченный набор.
        """
        readonly_fields = list(self.readonly_fields)

        # Если пользователь не суперпользователь, ограничиваем его возможности
        if not request.user.is_superuser:
            readonly_fields.extend(["is_superuser", "user_permissions", "groups"])

        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        """
        Определяет, может ли пользователь удалять записи.

        Обычные админы не могут удалять пользователей.
        """
        return request.user.is_superuser

    def get_queryset(self, request):
        """
        Оптимизирует запросы к базе данных для списка пользователей.

        Предзагружаем связанные объекты для избежания N+1 проблемы.
        """
        queryset = super().get_queryset(request)
        # Предзагружаем группы и права для оптимизации
        return queryset.prefetch_related("groups", "user_permissions")


# Настройка заголовков админки
admin.site.site_header = "🎯 Habits Tracker - Администрирование"
admin.site.site_title = "Habits Tracker Admin"
admin.site.index_title = "Добро пожаловать в панель администрирования"