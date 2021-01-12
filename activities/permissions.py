from rest_framework import permissions


class FacilitatorEditProtected(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or 'POST':
            return True

        return request.user and request.user.is_staff
