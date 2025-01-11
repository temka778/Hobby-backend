from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """Разрешает доступ только неавторизованным пользователям"""
    def has_permission(self, request, view):
        return not request.user.is_authenticated