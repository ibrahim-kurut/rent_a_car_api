from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit or delete cars.
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for any user (read-only access)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Otherwise, only allow access if the user is an admin
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the owner of the reservation or admin users
    to view, edit, or delete the reservation.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) only if the user is the owner or an admin
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff or obj.customer == request.user

        # For editing or deleting, allow only if the user is the owner or an admin
        return request.user.is_staff or obj.customer == request.user
