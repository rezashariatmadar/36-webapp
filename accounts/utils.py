import re
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrap(request, *args, **kwargs):
        from django.conf import settings
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.contrib.auth.views import redirect_to_login
        
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL, REDIRECT_FIELD_NAME)
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def barista_required(view_func):
    def wrap(request, *args, **kwargs):
        from django.conf import settings
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.contrib.auth.views import redirect_to_login

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL, REDIRECT_FIELD_NAME)
        if request.user.is_barista or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def customer_required(view_func):
    def wrap(request, *args, **kwargs):
        from django.conf import settings
        from django.contrib.auth import REDIRECT_FIELD_NAME
        from django.contrib.auth.views import redirect_to_login

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL, REDIRECT_FIELD_NAME)
        if request.user.is_customer:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrap
