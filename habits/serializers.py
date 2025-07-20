from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        """Дополнительная валидация."""
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Нельзя указывать одновременно связанную привычку и вознаграждение."
            )

        # Проверка времени выполнения
        if data.get("execution_time") and data["execution_time"] > 120:
            raise serializers.ValidationError(
                {"execution_time": "Время выполнения не должно превышать 120 секунд."}
            )

        # Проверка связанной привычки
        if data.get("related_habit") and not data["related_habit"].is_pleasant:
            raise serializers.ValidationError(
                {
                    "related_habit": "В связанные привычки могут попадать только приятные привычки."
                }
            )

        # Проверка приятной привычки
        if data.get("is_pleasant") and (
            data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # Проверка периодичности
        if data.get("periodicity") and data["periodicity"] > 7:
            raise serializers.ValidationError(
                {"periodicity": "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."}
            )

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "periodicity",
            "execution_time",
            "created_at",
        )
        read_only_fields = fields
