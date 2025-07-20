from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitListCreateView(generics.ListCreateAPIView):
    """Список привычек пользователя и создание новой привычки."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_pleasant', 'is_public']

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детальный просмотр, редактирование и удаление привычки."""

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек."""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    permission_classes = [permissions.IsAuthenticated]