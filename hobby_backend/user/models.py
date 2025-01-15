from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField('Почта', unique=True)
    avatar = models.ImageField('Ава', upload_to='avatars/', blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=150, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ForbiddenUsername(models.Model):
    word = models.CharField('Ник', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Запрещённый ник'
        verbose_name_plural = 'Запрещённые ники'

    def __str__(self):
        return self.word