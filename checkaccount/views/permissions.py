from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class CheckAccountPermission(BasePermission):
    def has_permission(self, request, view):
        # first check
        user_group = self.check_user_group(request)

        # also
        # ...
        if request.user.is_superuser:
            return True

        return user_group

    def check_user_group(self, request):
        if request.user and request.user.groups.filter(name='CheckAccountAdmin'):
            return True

        return False


