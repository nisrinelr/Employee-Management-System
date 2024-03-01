from rest_framework.permissions import BasePermission
from authentication.constants import HRMANAGER, EMPLOYEE, SUPERADMIN
from authentication.models import Employee
class IsSuperadmin(BasePermission):
    """
    Allows access only to super administrators.
    """
    message = "You must be a super administrator to access this resource."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == SUPERADMIN

class IsHRManager(BasePermission):
    """
    Allows access only to HR managers.
    """
    message = "You must be an HR manager to access this resource."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == HRMANAGER

class IsEmployee(BasePermission):
    """
    Allows access only to employees.
    """
    message = "You must be an employee to access this resource."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == EMPLOYEE
