from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from user.models import CustomUser as User


class SignupView(APIView):
    """ Регистрация пользователя """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Пользователь успешно создан"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """Получение и редактирование данных пользователя (по id или username)"""
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, identifier):
        """Получить объект пользователя по id или username"""
        lookup_field = "id" if identifier.isdigit() else "username"
        return get_object_or_404(User, **{lookup_field: identifier})

    def get(self, request, identifier):
        """Получение данных пользователя"""
        user = self.get_object(identifier)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, identifier):
        """Редактирование данных пользователя"""
        user = self.get_object(identifier)
        if request.user != user:
            return Response({"error": "Вы можете редактировать только свою страницу."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    """ Выход пользователя из учётки """
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавляем токен в черный список
            return Response({"message": "Ты успешно вышел из учётки"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)