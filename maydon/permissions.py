from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'user':
            if request.method in permissions.SAFE_METHODS:
                return True
            elif request.method == 'POST':
                return True
            else:
                return False
        if request.user.role == 'owner':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'user':
            if request.method in permissions.SAFE_METHODS:
                return True
            if request.method == 'POST':
                return True
        if request.user.role == 'owner':
            return obj.owner == request.user or obj.maydon.owner == request.user

        return False
