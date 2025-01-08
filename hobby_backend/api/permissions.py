from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее только владельцу редактировать данные,
    но разрешающее чтение всем пользователям.
    """
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешить редактирование только владельцу
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or obj.id == request.user.id