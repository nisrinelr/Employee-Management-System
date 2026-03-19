from functools import wraps
from django.http import HttpResponse
from authentication.constants import SUPERADMIN, HRMANAGER

def has_permission(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_superuser or request.user.user_type in ['0', '1', SUPERADMIN, HRMANAGER]):
            return HttpResponse("You don't have the permission to access this page.", status=403)
        return view_func(request, *args, **kwargs)
    return wrapper