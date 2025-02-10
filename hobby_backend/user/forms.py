from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя в админке"""
    class Meta:
        model = CustomUser
        fields = ("email",)  # Только email, username не нужен

    def clean_username(self):
        return None  # Возвращаем None, чтобы не сохранялось в БД


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пользователя в админке"""
    class Meta:
        model = CustomUser
        fields = "__all__"  # Оставляем возможность редактировать все поля
