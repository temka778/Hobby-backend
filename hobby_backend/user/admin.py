from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ForbiddenUsername
from .forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'pk', 'email', 'username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'avatar', 'is_staff')
    
    form = CustomUserChangeForm

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ForbiddenUsername)