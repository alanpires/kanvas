from rest_framework import permissions

class IsInstructorOrFacilitator(permissions.BasePermission):
    def has_permission(self, request, view):       
        return request.user and request.user.is_staff
    
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff == False and request.user.is_superuser == False