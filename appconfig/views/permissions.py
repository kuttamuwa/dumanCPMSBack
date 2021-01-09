from rest_framework.permissions import BasePermission


class DomainPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Only super user can change domain and subtypes
        :param request:
        :param view:
        :return:
        """
        if request.user.is_superuser:
            return True

        return False


class SubtypePermission(BasePermission):
    def has_permission(self, request, view):
        """
        Only super user can change domain and subtypes
        :param request:
        :param view:
        :return:
        """
        if request.user.is_superuser:
            return True

        return False

