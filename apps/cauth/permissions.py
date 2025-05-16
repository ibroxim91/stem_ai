from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    """
    Faqat admin roliga ega foydalanuvchilargina ruxsat oladi.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
