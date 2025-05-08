from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite registrar sin autenticación
def register_view(request):
    """
    Registra un usuario nuevo y retorna su token.
    Espera:
      {
        "username": "...",
        "email": "...",  // opcional
        "password": "..."
      }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Generar token automáticamente
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    else:
        # Devuelve detalles de los campos que fallan
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(ObtainAuthToken):
    """
    Endpoint de login. Retorna el token, user_id y username.
    Espera:
      {
        "username": "...",
        "password": "..."
      }
    """
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        # response.data debería contener {"token": "..."} si el login es exitoso
        if 'token' in response.data:
            token = Token.objects.get(key=response.data['token'])
            user = token.user
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        else:
            # Si no hay 'token', probablemente sean credenciales inválidas
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    """
    Logout. Elimina el token del usuario autenticado, forzando que no pueda seguir usándolo.
    """
    user = request.user
    if not user.is_authenticated:
        return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    # Borramos el token, de manera que ya no tenga acceso
    Token.objects.filter(user=user).delete()
    return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
