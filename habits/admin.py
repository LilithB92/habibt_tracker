from django.contrib import admin

from habits.models import Habit


# Register your models here.
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Администрирование модели Привычек.
    Супер пользователю позволяет управлять привычками.
    """

    list_display = (
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
    )
