from rest_framework import permissions


class EndPointRestrict(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True


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


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class IsStaff(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_staff or request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff and request.method not in self.edit_methods:
            return True


class CreatorAllStaffAllButEditOrReadOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # print(obj, "===========obj==============")
        print(obj.series.creator.creator, "obj================================")
        print(request.user, "===================user making request============")
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.series.creator.creator == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
