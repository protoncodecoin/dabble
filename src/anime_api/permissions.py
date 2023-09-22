from rest_framework import permissions


class IsCreatorOrReaOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permisssions are only allowed to the author of the
        print("creator is: ", obj.creator)
        return obj.creator == request.user
