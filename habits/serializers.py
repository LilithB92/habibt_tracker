from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели «Курс».

    Обрабатывает преобразование экземпляров Привычек в формат JSON и выполняет валидацию
    входящие данные для удаления, создания или обновления привычек.
    """

    class Meta:
        model = Habit
        fields = (
            "pk",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "created_at", "updated_at")

    def validate(self, data):
        # 1. Проверка: Связанная привычка + Вознаграждение
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")

        # 2. Проверка: Приятная привычка не может иметь связанной или награды
        if data.get("is_pleasant"):
            if data.get("related_habit") or data.get("reward"):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть связанной привычки или вознаграждения."
                )

        # 3. Проверка: Время выполнения (не более 120 сек)
        if data.get("duration") and data.get("duration").total_seconds() > 120:
            raise serializers.ValidationError("Время выполнения должно быть не более 120 секунд.")

        # 4. Проверка: Периодичность
        if data.get("periodicity", 1) > 7:
            raise serializers.ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

        return data
