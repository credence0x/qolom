from rest_framework.permissions import BasePermission

class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_related_business_profile_object()


class IsBusinessOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.businessProfile == obj.owner
