from rest_framework.permissions import BasePermission

class IsEndUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_related_user_profile_object()

class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.userProfile == obj.owner


