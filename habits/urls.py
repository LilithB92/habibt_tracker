from rest_framework import routers

from habits.apps import HabbitsConfig
from habits.views import HabitViewSet

app_name = HabbitsConfig.name

router = routers.SimpleRouter()
router.register(r"", HabitViewSet, basename="habit")

urlpatterns = []

urlpatterns += router.urls
