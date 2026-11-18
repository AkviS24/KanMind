from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from ..models import User
from .serializers import LoginSerializer, EmailCheckSerializer


class LoginView(APIView):
    """Handle user authentication and token retrieval."""

    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

    def post(self, request):
        """Authenticate the configured demo user and return a token."""
        if settings.KANMIND_LOGIN_DISABLED:
            return Response(
                {"detail": "Login is disabled on this backend."},
                status=status.HTTP_403_FORBIDDEN,
            )

        submitted_email = (
            request.data.get("email", "")
            if hasattr(request.data, "get")
            else ""
        )
        if (
            settings.KANMIND_GUEST_ONLY_LOGIN
            and submitted_email.strip().lower()
            != settings.KANMIND_GUEST_EMAIL
        ):
            return Response(
                {"detail": "Only the configured demo account is available."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'token': token.key,
                    'fullname': user.fullname,
                    'email': user.email,
                    'user_id': user.id,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class EmailCheckView(APIView):
    """Handle authenticated requests for user email lookups."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return basic user information for a given email address."""
        serializer = EmailCheckSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(
            User,
            email=serializer.validated_data['email'],
        )

        return Response(
            {
                'id': user.id,
                'email': user.email,
                'fullname': user.fullname,
            },
            status=status.HTTP_200_OK,
        )
