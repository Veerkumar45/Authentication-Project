# users/views.py
import random
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserSerializer, RegisterSerializer, VerifyOTPSerializer, LoginSerializer
)
from .models import EmailOTP, AuthToken
from django.utils import timezone
from django.core.mail import send_mail

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf(request):
    """
    Call this endpoint (or open Swagger) to ensure csrftoken cookie is set.
    """
    return Response({'csrfToken': get_token(request)})

@swagger_auto_schema(method='post', request_body=RegisterSerializer, security=[{'X-CSRFToken': []}])
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    s = RegisterSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    email = s.validated_data['email'].lower()
    password = s.validated_data['password']

    user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'is_active': False})
    if not created and user.is_active:
        return Response({'detail': 'User already exists and is active.'}, status=400)

    if created:
        user.set_password(password)
        user.is_active = False
        user.save()

    code = f'{random.randint(0, 999999):06d}'
    EmailOTP.objects.create(email=email, code=code)

    send_mail(
        subject='Your verification code',
        message=f'Your OTP is {code}. It expires in 10 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )
    return Response({'detail': 'OTP sent to email. Use /api/register/verify to activate.'}, status=201)

@swagger_auto_schema(method='post', request_body=VerifyOTPSerializer, security=[{'X-CSRFToken': []}])
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_registration(request):
    s = VerifyOTPSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    email = s.validated_data['email'].lower()
    code = s.validated_data['code']

    try:
        otp = EmailOTP.objects.filter(email=email, is_used=False).latest('created')
    except EmailOTP.DoesNotExist:
        return Response({'detail': 'No OTP found. Please register again.'}, status=400)

    if otp.is_used or otp.is_expired() or otp.code != code:
        return Response({'detail': 'Invalid or expired OTP.'}, status=400)

    otp.is_used = True
    otp.save()

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=404)

    user.is_active = True
    user.save()
    return Response({'detail': 'Registration verified. You can now log in.'}, status=200)

@swagger_auto_schema(method='post', request_body=LoginSerializer, security=[{'X-CSRFToken': []}])
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    s = LoginSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    email = s.validated_data['email'].lower()
    password = s.validated_data['password']

    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        return Response({'detail': 'Account not verified.'}, status=403)

    token = AuthToken.objects.create(
        user=user,
        key=AuthToken.generate(),
        expires_at=timezone.now() + timedelta(days=1)
    )

    resp = Response({'detail': 'Logged in.', 'expires_at': token.expires_at})
    resp.set_cookie(
        key='auth_token',
        value=token.key,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=24 * 60 * 60,
        path='/'
    )
    return resp

@api_view(['GET'])
def me(request):
    return Response(UserSerializer(request.user).data)

@swagger_auto_schema(method='post', security=[{'X-CSRFToken': []}])
@api_view(['POST'])
def logout(request):
    token_key = request.COOKIES.get('auth_token')
    if token_key:
        AuthToken.objects.filter(key=token_key).delete()
    resp = Response({'detail': 'Logged out.'})
    resp.delete_cookie('auth_token', path='/')
    return resp
