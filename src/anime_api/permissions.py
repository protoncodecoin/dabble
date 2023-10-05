from rest_framework import permissions


class IsCreatorMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.groups.filter(name="creator").exists()
        ):
            return True
        return False


class IsCommonUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="common_user").exists():
            return True
        return False


class CreatorAllStaffAllButEditOrReadOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.creator == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
