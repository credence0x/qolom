from rest_framework.permissions import BasePermission

class BusinessOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_business_profile_object()

