from rest_framework import serializers
from user.models import CustomUser as User

class SignupSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации пользователя """
    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        # Создание пользователя с хэшированием пароля
        user = User.objects.create_user(**validated_data)
        return user
