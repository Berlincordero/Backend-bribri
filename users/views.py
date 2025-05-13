from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegisterSerializer


# ─────────────── REGISTRO ───────────────
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user_id": user.id,
                "username": user.username,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────── LOGIN ───────────────
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "token" in response.data:
            token = Token.objects.get(key=response.data["token"])
            user  = token.user
            return Response(
                {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ─────────────── LOGOUT ───────────────
@api_view(["POST"])
def logout_view(request):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {"detail": "User is not authenticated"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    Token.objects.filter(user=user).delete()
    return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

