from django.contrib.auth.models import AnonymousUser
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


class CookieTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get auth_token from cookie
        token = request.COOKIES.get("auth_token")
        if not token:
            return None

        # CSRF check
        self._enforce_csrf(request)

        # Attach user (for now we keep it simple, since you’re storing user in session/cookie)
        user = getattr(request, "user", AnonymousUser())
        if not user or user.is_anonymous:
            raise exceptions.AuthenticationFailed("Invalid session or user not authenticated")

        return (user, None)

    def _enforce_csrf(self, request):
        """Ensure CSRF protection is applied properly."""
        csrf_middleware = CsrfViewMiddleware(lambda req: None)
        reason = csrf_middleware.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")
