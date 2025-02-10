from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """ Менеджер для модели CustomUser """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Почта обязательна, она может пригодиться для восстановления пароля')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.update({'is_staff': True, 'is_superuser': True})
        return self.create_user(email, password, **extra_fields)