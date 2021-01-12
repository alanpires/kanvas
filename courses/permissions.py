from rest_framework import permissions
import ipdb


class WriteProtected(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated


class FacilitatorEditProtected(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return request.user and request.user.is_staff


class InstructorWriteProtected(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return request.user and request.user.is_superuser
