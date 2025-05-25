from rest_framework import permissions


class IsSuperuserOrSystemAdmin(permissions.BasePermission):
    """
    Доступ разрешён, если пользователь:
    • суперпользователь (`is_superuser=True`);
    • состоит в группе «Администратор системы»;
    • состоит в группе «Модератор».
    """

    SYSTEM_ADMIN_GROUP = "Администратор системы"
    MODERATOR_GROUP = "Модератор"

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(
            name__in=[self.SYSTEM_ADMIN_GROUP, self.MODERATOR_GROUP]
        ).exists()