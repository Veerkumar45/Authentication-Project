# users/auth.py
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import AuthToken

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class CookieTokenAuthentication(BaseAuthentication):
    """
    Reads 'auth_token' from request.COOKIES and enforces CSRF for unsafe methods.
    """
    cookie_name = 'auth_token'

    def authenticate(self, request):
        token_key = request.COOKIES.get(self.cookie_name)
        if not token_key:
            return None  # no cookie => unauthenticated

        # Enforce CSRF for unsafe methods
        if request.method not in SAFE_METHODS:
            self._enforce_csrf(request)

        try:
            token = AuthToken.objects.select_related('user').get(key=token_key)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid auth token.')

        if token.is_expired():
            token.delete()
            raise exceptions.AuthenticationFailed('Auth token expired. Please log in again.')

        return (token.user, token)

    def _enforce_csrf(self, request):
        reason = CsrfViewMiddleware().process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')
