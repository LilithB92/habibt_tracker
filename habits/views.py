from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек"""

    serializer_class = HabitSerializer

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        return Habit.objects.filter(user=self.request.user).order_by('pk')

    def perform_create(self, serializer):
        """При создании привычки поле для владельца сущности заполняется аутентифицированным пользователем."""
        serializer.save(user=self.request.user)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """  Представление для публичных привычек, только для просмотра """
    serializer_class = HabitSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Пользователь видит только публичные привычки"""
        return Habit.objects.filter(is_public=True).order_by('pk')
