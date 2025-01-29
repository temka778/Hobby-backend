from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ForbiddenUsername
from .forms import CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm

    list_display = (
        "pk", "email", "username", "first_name", "middle_name", "last_name", "birth_date", "avatar", "is_staff"
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("username", "first_name", "middle_name", "last_name", "birth_date", "avatar")}),
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ForbiddenUsername)
