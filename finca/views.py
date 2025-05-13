from rest_framework import viewsets, permissions
from rest_framework.parsers import (
    JSONParser, MultiPartParser, FormParser,
)
from rest_framework.response import Response

from .models      import Profile, Post
from .serializers import ProfileSerializer, PostSerializer


class IsOwner(permissions.BasePermission):
    """Solo el dueño de Profile puede editarlo."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthor(permissions.BasePermission):
    """Solo el autor puede modificar / borrar su Post."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


# ---------- PERFIL ----------
class MyFincaViewSet(viewsets.ModelViewSet):
    serializer_class   = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        perfil, _ = Profile.objects.get_or_create(user=self.request.user)
        return perfil

    def list(self, request, *args, **kwargs):
        ser = self.get_serializer(self.get_object())
        return Response(ser.data)

    # POST → alias de update (para formulario <multipart>)
    def create(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# ---------- POSTS ----------
class PostViewSet(viewsets.ModelViewSet):
    """
    /api/finca/posts/
      GET      → lista mis posts
      POST     → crea un post (JSON text | multipart text+media)
    /api/finca/posts/<id>/
      PATCH    → edita texto
      DELETE   → mueve a “reciclaje” (elimina)
    """
    serializer_class   = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    parser_classes     = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
