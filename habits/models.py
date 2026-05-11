from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Сохраняет одну запись о привычках, связанную с собой и с:model:`users.User`"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")

    # Связанная привычка (только для полезных)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        limit_choices_to={"is_pleasant": True},  # Только приятные в связке
    )

    # Периодичность (по умолчанию ежедневная - 1)
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")

    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")

    duration = models.DurationField(verbose_name="Время на выполнение (сек/мин)")
    is_public = models.BooleanField(default=False, verbose_name="Публичность")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
