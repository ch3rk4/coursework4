from django.urls import path

from .views import connect_telegram, disconnect_telegram

app_name = "telegram_bot"

urlpatterns = [
    path("telegram/connect/", connect_telegram, name="connect-telegram"),
    path("telegram/disconnect/", disconnect_telegram, name="disconnect-telegram"),
]
