from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ForbiddenUsername
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """Админка для пользователей с email вместо username"""
    model = CustomUser
    add_form = CustomUserCreationForm  # Форма создания
    form = CustomUserChangeForm  # Форма редактирования

    list_display = ("pk", "email", "username", "first_name", "middle_name", "last_name", "birth_date", "avatar", "is_staff")
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("username", "first_name", "middle_name", "last_name", "birth_date", "avatar")}),
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    ordering = ("email",)
    search_fields = ("email", "username")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ForbiddenUsername)
