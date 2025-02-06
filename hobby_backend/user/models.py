from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField('Почта', unique=True)
    avatar = models.ImageField('Ава', upload_to='avatars/', blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=150, blank=True, null=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    username = models.CharField('Никнейм', max_length=150, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """Гарантируем уникальность username перед сохранением"""
        if self.username:
            self.username = self.username.strip() or None  # Чистим пробелы, заменяем пустую строку на None
            if CustomUser.objects.filter(username=self.username).exclude(pk=self.pk).exists():
                raise ValueError(f"Username '{self.username}' уже используется.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class ForbiddenUsername(models.Model):
    word = models.CharField('Ник', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Запрещённый ник'
        verbose_name_plural = 'Запрещённые ники'

    def __str__(self):
        return self.word