from django.urls import path

from .views import HabitDetailView, HabitListCreateView, PublicHabitListView

app_name = "habits"

urlpatterns = [
    path("habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("habits/public/", PublicHabitListView.as_view(), name="public-habits"),
]
