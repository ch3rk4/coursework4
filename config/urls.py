from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.decorators import api_view
from rest_framework.response import Response

urlpatterns = [
    # Админ панель
    path("admin/", admin.site.urls),
    # API документация
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Аутентификация (Djoser + JWT)
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # Основные API endpoints
    path("api/", include("habits.urls")),
    path("api/", include("telegram_bot.urls")),
]

# Статические файлы для разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


@api_view(["GET"])
def api_root(request):
    """
    Корневой endpoint API трекера привычек.

    Добро пожаловать в API трекера полезных привычек! 🎯
    """
    return Response(
        {
            "message": "🎯 Добро пожаловать в Habits Tracker API!",
            "version": "1.0.0",
            "endpoints": {
                "🏠 Habits API": {
                    "list_create": "/api/habits/",
                    "detail": "/api/habits/{id}/",
                    "public": "/api/habits/public/",
                },
                "👤 Authentication": {
                    "register": "/api/auth/users/",
                    "login": "/api/auth/jwt/create/",
                    "refresh": "/api/auth/jwt/refresh/",
                    "verify": "/api/auth/jwt/verify/",
                    "user_profile": "/api/auth/users/me/",
                },
                "🤖 Telegram": {
                    "connect": "/api/telegram/connect/",
                    "disconnect": "/api/telegram/disconnect/",
                },
                "📖 Documentation": {
                    "swagger": "/api/docs/",
                    "redoc": "/api/redoc/",
                    "schema": "/api/schema/",
                },
            },
            "features": [
                "🔐 JWT аутентификация",
                "📝 CRUD операции с привычками",
                "🔔 Telegram уведомления",
                "🌍 Публичные привычки",
                "⏰ Автоматические напоминания",
                "📊 Фильтрация и пагинация",
            ],
        }
    )


# Добавляем корневой маршрут
urlpatterns.insert(-2 if settings.DEBUG else 0, path("api/", api_root, name="api-root"))
