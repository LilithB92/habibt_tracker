import secrets

from rest_framework import generics
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserGeneralInformationSerializer
from users.serializers import UserSerializer
from users.serializers import UserUpdateSerializer
from users.services import EmailVerification


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя с верификацией почтой"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = secrets.token_hex(16)
        user.verification_token = token
        user.set_password(user.password)
        user.save()
        request = self.request
        EmailVerification.authentication_by_email(request=request, token=token, user_email=user.email)


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        try:
            print(token)
            user = User.objects.filter(verification_token=token).first()
            if user:
                print(user.email)
                user.is_active = True
                user.verification_token = None
                user.save()
            return Response({"message": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid verification token."}, status=status.HTTP_400_BAD_REQUEST)


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
