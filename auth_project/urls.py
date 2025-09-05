from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.http import JsonResponse
from django.middleware.csrf import get_token

def swagger_csrf_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version="v1",
        description="API documentation for authentication system",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),

    # ✅ Swagger + ReDoc endpoints
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger/csrf/", swagger_csrf_view, name="swagger-csrf"),
]
