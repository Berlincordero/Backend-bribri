from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    # Sobrescribimos password para que sea de solo escritura y no aparezca en GET
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Extraemos username, email y password
        username = validated_data['username']
        email = validated_data.get('email', '')
        password = validated_data['password']

        # Creamos instancia
        user = User(username=username, email=email)
        # Encriptamos la contraseña
        user.set_password(password)
        user.save()
        return user
