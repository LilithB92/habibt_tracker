from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView
from users.views import UserDestroyAPIView
from users.views import UserListApiView
from users.views import UserRetrieveAPIView
from users.views import UserUpdateAPIView
from users.views import VerifyEmailView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("list/", UserListApiView.as_view(), name="user_list"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="delete"),
]
