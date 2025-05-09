from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'admin'

class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type in ['admin', 'staff']

class IsDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'donor'

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'staff'

class IsAdminOrStaffOrDonor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type in ['admin', 'staff', 'donor']

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'admin' or obj.user == request.user 