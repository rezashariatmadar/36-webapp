from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def spa_shell(request, path=None):
    return render(request, "app.html")
