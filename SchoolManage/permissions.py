# permissions.py
from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'teacher' role
        return request.user.role == 'Teacher' and request.user.is_active
        
  