from django.urls import path
from . import views

urlpatterns = [
    path("csrf/", views.get_csrf, name="csrf"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/verify/", views.VerifyRegisterView.as_view(), name="verify-register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.me, name="me"),
]
