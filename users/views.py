from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView

from users.models import User
from users.serializers import UserGeneralInformationSerializer
from users.serializers import UserSerializer
from users.serializers import UserUpdateSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """Получение списка пользователей"""

    queryset = User.objects.all()
    serializer_class = UserGeneralInformationSerializer
    # permission_classes = (IsAuthenticated,)


class UserRetrieveAPIView(RetrieveAPIView):
    """Получение одной сущности пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """просмотра чужого профиля должна быть доступна только общая информация, а в собственном вся"""
        if self.request.user.id == self.kwargs.get("pk"):
            return UserSerializer
        return UserGeneralInformationSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменение одной сущности пользователя"""

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    # permission_classes = (IsAuthenticated, IsUserOwner)

    def perform_update(self, serializer):
        """Метод serializer.save() вызывает метод .update(), определенный в UserUpdateSerializer."""
        serializer.save()


class UserDestroyAPIView(DestroyAPIView):
    """Удаление одной сущности пользователя"""

    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated, IsUserOwner)
