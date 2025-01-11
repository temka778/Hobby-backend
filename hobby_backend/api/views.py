from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsNotAuthenticated
from .serializers import SignupSerializer, UserSerializer
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


class CurrentUserView(APIView):
    """Запрос, просмотр и изменение текущего пользователя"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """Запрос и просмотр пользователя по ID или username"""
    permission_classes = [AllowAny]
    def get(self, request, id=None, username=None):
        if id:
            user = get_object_or_404(User, id=id)
        elif username:
            user = get_object_or_404(User, username=username)
        else:
            return Response({"error": "ID или username должны быть указаны"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LogoutView(APIView):
    """ Выход пользователя из учётки """
    permission_classes = [IsAuthenticated]
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