from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import random

User = get_user_model()

# In-memory OTP store (use cache/DB in production)
otp_store = {}

# ---------------- CSRF ----------------
@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})


# ---------------- Register ----------------
@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        import json

        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"detail": "Email and password required."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"detail": "Email already registered."}, status=400)

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            otp_store[email] = {"otp": otp, "password": password}

            print(f"📩 OTP for {email}: {otp}")  # Simulating email sending
            return JsonResponse({"detail": "OTP sent to email (check console)."})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)


# ---------------- Verify Registration ----------------
@method_decorator(csrf_exempt, name="dispatch")
class VerifyRegisterView(View):
    def post(self, request):
        import json

        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")

            if not email or not otp:
                return JsonResponse({"detail": "Email and OTP required."}, status=400)

            if email not in otp_store:
                return JsonResponse({"detail": "No pending registration for this email."}, status=400)

            if otp_store[email]["otp"] != otp:
                return JsonResponse({"detail": "Invalid OTP."}, status=400)

            # Create user
            password = otp_store[email]["password"]
            user = User.objects.create_user(username=email, email=email, password=password)
            del otp_store[email]

            return JsonResponse({"detail": "Registration successful."})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)


# ---------------- Login ----------------
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        import json

        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"detail": "Email and password required."}, status=400)

            user = authenticate(request, username=email, password=password)
            if user is None:
                return JsonResponse({"detail": "Invalid credentials."}, status=400)

            login(request, user)
            return JsonResponse({"detail": "Login successful."})
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)


# ---------------- Logout ----------------
@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"detail": "Logged out."})


# ---------------- Me (protected) ----------------
@login_required
def me(request):
    user = request.user
    return JsonResponse({
        "id": user.id,
        "email": user.email,
        "username": user.username,
    })
