
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsGroupAdmin(BasePermission):
    """
    The request is for group admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and request.user.group_creator.id
        )
