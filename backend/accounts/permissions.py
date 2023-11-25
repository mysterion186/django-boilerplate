"""Create a custom perssions in order to force the user to authenticate."""
from rest_framework.permissions import BasePermission
from .models import MyUser

class CustomIsAuthenticated(BasePermission):
    """Check that all the user's field are not null."""

    def has_permission(self, request, view):
        """Handle the permission logic."""
        user: MyUser = request.user
        # don't handle not authenticated user
        if not user.is_authenticated:
            return False
        return user.is_complete
