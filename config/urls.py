from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Habits API",
      default_version='v1',
      description="Test Project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="bichakhchyanlilith1992@gmail.com"),
      license=openapi.License(name="without license"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("users/", include("users.urls", namespace="users")),
    path("habits/", include("habits.urls", namespace="habits")),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
