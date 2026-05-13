from django.urls import path
from rest_framework import routers

from habits.apps import HabbitsConfig
from habits.views import HabitViewSet
from habits.views import PublicHabitViewSet

app_name = HabbitsConfig.name

router = routers.SimpleRouter()
router.register(r"", HabitViewSet, basename="habit")


urlpatterns = [
    path('public_habit/', PublicHabitViewSet.as_view({'get': 'list'}), name="public_habit_list"),
    path('public_habit/<int:pk>/', PublicHabitViewSet.as_view({'get': 'retrieve'}),  name="public_habit_retrieve"),
]

urlpatterns += router.urls
