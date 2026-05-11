from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView
from users.views import UserDestroyAPIView
from users.views import UserListApiView
from users.views import UserRetrieveAPIView
from users.views import UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("list/", UserListApiView.as_view(), name="user_list"),
    path("detail/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="delete"),
]
