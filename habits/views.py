from rest_framework import viewsets

from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек"""

    serializer_class = HabitSerializer

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привычки поле для владельца сущности заполняется аутентифицированным пользователем."""
        serializer.save(user=self.request.user)
        serializer.save()
