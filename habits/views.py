from celery.exceptions import CeleryError
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import PeriodicTasks
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Habit
from .serializers import HabitSerializer
from .services import HabitPeriodicTask


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек"""

    serializer_class = HabitSerializer

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        return Habit.objects.filter(user=self.request.user.id).order_by("pk")

    def perform_create(self, serializer):
        """При создании привычки поле для владельца сущности заполняется аутентифицированным пользователем
        и создает объект периодического задании"""
        habit = serializer.save(user=self.request.user)
        try:
            schedule = HabitPeriodicTask.set_schedule(habit=habit)
            HabitPeriodicTask.set_crontab(habit=habit, crontab_schedule=schedule)
        except Exception as e:
            raise CeleryError(f"Task failed with: {e}")

    def perform_update(self, serializer):
        """При обновлении привычки поле для владельца сущности и создает новый объект периодического задании"""
        habit = serializer.save()
        task = PeriodicTask.objects.filter(name=habit.action).first()
        if task:
            task.delete()
        try:
            schedule = HabitPeriodicTask.set_schedule(habit=habit)
            HabitPeriodicTask.set_crontab(habit=habit, crontab_schedule=schedule)
        except Exception as e:
            raise CeleryError(f"Task failed with: {e}")

    def perform_destroy(self, instance):
        """Когда удаляем привычку автоматический удаляется график привычки"""
        action = instance.action
        instance.delete()
        task = PeriodicTask.objects.filter(name=action).first()
        if task:
            task.delete()
            PeriodicTasks.changed(task)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для публичных привычек, только для просмотра"""

    serializer_class = HabitSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Пользователь видит только публичные привычки"""
        return Habit.objects.filter(is_public=True).order_by("pk")
