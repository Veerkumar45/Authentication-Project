# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.csrf, name='csrf'),
    path('register/', views.register, name='register'),
    path('register/verify/', views.verify_registration, name='verify'),
    path('login/', views.login, name='login'),
    path('me/', views.me, name='me'),
    path('logout/', views.logout, name='logout'),
]
