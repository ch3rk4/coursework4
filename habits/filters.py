import django_filters

from .models import Habit


class HabitFilter(django_filters.FilterSet):
    """Фильтр для привычек."""

    action = django_filters.CharFilter(lookup_expr="icontains")
    place = django_filters.CharFilter(lookup_expr="icontains")
    is_pleasant = django_filters.BooleanFilter()
    is_public = django_filters.BooleanFilter()

    class Meta:
        model = Habit
        fields = ["action", "place", "is_pleasant", "is_public"]
