from rest_framework import permissions

class AuthorizationPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            return False
        return True
        