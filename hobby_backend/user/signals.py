from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken

@receiver(post_save, sender=User)
def update_user_token(sender, instance, **kwargs):
    """
    Обновляет токен пользователя после изменения его данных.
    """
    if not kwargs.get('created', False):  # Только при обновлении
        refresh = RefreshToken.for_user(instance)
        refresh['username'] = instance.username