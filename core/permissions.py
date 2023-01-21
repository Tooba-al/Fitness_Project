from rest_framework.permissions import BasePermission
from .models import *
from django.utils.translation import gettext as _

def is_authenticated(request):
    if not (request.user and request.user.is_authenticated):
        return False

    try:
        request.user.user_profile
        return True
    except UserProfile.DoesNotExist:
        return False

class IsAuthenticated(BasePermission):
    message = _("You need to log in.")

    def has_permission(self, request, view):
        if is_authenticated(request):
            return True

        return False