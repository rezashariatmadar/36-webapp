import re
from django.core.exceptions import PermissionDenied

def normalize_digits(text):
    """
    Normalizes Persian and Arabic digits to ASCII digits.
    """
    if not isinstance(text, str):
        return text
    
    # Mapping of Persian/Arabic digits to ASCII
    mapping = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    
    return ''.join(mapping.get(char, char) for char in text)

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
