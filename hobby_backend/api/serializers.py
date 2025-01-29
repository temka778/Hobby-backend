from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import CustomUser as User
from user.models import ForbiddenUsername


class SignupSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации пользователя """
    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        """Создание пользователя"""
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Сериализатор для получения токена """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для пользователя """
    
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "middle_name", "birth_date", "avatar"
        ]
        read_only_fields = ["id", "email"]

    def validate_username(self, value):
        """Проверка имени пользователя: уникальность, запрещённые слова"""
        if value:
            value = value.strip()  # Убираем пробелы в начале и конце
            
            # Проверяем запрещённые слова
            forbidden_words = ForbiddenUsername.objects.values_list("word", flat=True)
            if any(word in value.lower() for word in forbidden_words):
                raise serializers.ValidationError(f"Имя пользователя '{value}' содержит запрещённое слово.")
            
            # Проверяем уникальность (исключаем текущего пользователя из проверки)
            user_id = self.instance.id if self.instance else None
            if User.objects.filter(username=value).exclude(id=user_id).exists():
                raise serializers.ValidationError("Этот username уже занят.")

        return value or None  # Возвращаем None, если поле пустое
