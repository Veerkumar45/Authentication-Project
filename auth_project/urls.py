"""
URL configuration for auth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import ensure_csrf_cookie

schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version='v1',
        description="Cookie-based authentication with CSRF protection",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Redirect homepage (/) to Swagger
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),

    path('admin/', admin.site.urls),

    # All user/auth routes under /api/
    path('api/', include('users.urls')),

    # Swagger documentation
    re_path(
        r'^swagger/$',
        ensure_csrf_cookie(schema_view.with_ui('swagger', cache_timeout=0)),
        name='schema-swagger-ui'
    ),

    # Optional: Redoc documentation
    re_path(
        r'^redoc/$',
        ensure_csrf_cookie(schema_view.with_ui('redoc', cache_timeout=0)),
        name='schema-redoc'
    ),
]
