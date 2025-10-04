from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import RoleNames


class ResumePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.role:
            return False

        # Получаем все разрешения роли в виде списка
        role_perms = user.role.permissions.values_list("codename", flat=True)
        print('role_perms', role_perms)
        print('user_role', user.role)
        print(request.method)

        if request.method in SAFE_METHODS:
            return "view_resume" in role_perms
        elif request.method == "POST":
            print('add_perm in role_perms', "add_resume" in role_perms)
            return "add_resume" in role_perms
        elif request.method in ("PUT", "PATCH"):
            return "change_resume" in role_perms
        elif request.method == "DELETE":
            return "delete_resume" in role_perms

        return False


    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role.name == RoleNames.HR_MANAGER.value:
            return True

        if user.role.name == RoleNames.CANDIDATE.value:
            return obj.user == user

