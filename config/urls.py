from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include
from django.urls import path

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("users/", include("users.urls", namespace="users")),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
