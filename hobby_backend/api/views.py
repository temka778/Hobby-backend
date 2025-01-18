from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsNotAuthenticated
from .serializers import SignupSerializer, UserSerializer, CustomTokenObtainPairSerializer
from user.models import CustomUser as User


def home(request):
    """Домашняя страница"""
    return HttpResponse("Здесь будет документация по API")


class SignupView(APIView):
    """ Регистрация пользователя """
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Пользователь успешно создан"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(APIView):
    """
    Универсальный эндпоинт для получения и редактирования данных пользователя.
    - GET: Просмотр страницы пользователя (по ID или username).
    - PUT/PATCH: Редактирование профиля авторизованным пользователем.
    """
    def get_permissions(self):
        """Получение прав доступа"""
        if self.request.method in ["GET"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, lookup):
        """Получение пользователя по ID или username"""
        try:
            if lookup.isdigit():
                """Если lookup - число, то это ID пользователя"""
                return get_object_or_404(User, id=int(lookup))
            """Иначе это username"""
            return get_object_or_404(User, username=lookup)
        except ValueError:
            return None

    def get(self, request, lookup):
        """Получение данных пользователя"""
        user = self.get_object(lookup)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, lookup):
        """Редактирование данных пользователя"""
        user = self.get_object(lookup)
        if user != request.user:
            return Response({"error": "Редактировать можно только свой профиль"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            # Генерация новых токенов
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
    
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, lookup):
        """Частичное редактирование данных пользователя"""
        user = self.get_object(lookup)
        if user != request.user:
            return Response({"error": "Редактировать можно только свой профиль"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    """ Выход пользователя из учётки """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Ты успешно вышел из учётки"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Ошибка выхода: {e}")  # Логирование ошибки
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)