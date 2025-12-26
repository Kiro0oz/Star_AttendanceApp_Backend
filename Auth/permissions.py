from rest_framework import permissions

class IsCommitteeAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and 
                    request.user.is_authenticated and 
                    request.user.role == 'admin')

class IsAdminOfTargetCommittee(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Admins can manage only their own committee's sessions.
        return obj.committee == request.user.committee