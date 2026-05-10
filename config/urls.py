from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path
from django.urls import include

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls"))
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()