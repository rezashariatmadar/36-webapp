import re
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def validate_iranian_national_id(national_id: str) -> bool:
    """Validates an Iranian National ID (Code Melli)."""
    if not re.match(r'^\d{10}$', national_id):
        return False
    check_digit = int(national_id[9])
    if len(set(national_id)) == 1:
        return False
    sum_digits = sum(int(national_id[i]) * (10 - i) for i in range(9))
    remainder = sum_digits % 11
    if remainder < 2:
        return check_digit == remainder
    else:
        return check_digit == (11 - remainder)

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
