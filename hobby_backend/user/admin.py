from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'pk', 'email', 'username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'avatar', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)