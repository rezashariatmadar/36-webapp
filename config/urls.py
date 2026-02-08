from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from theme.views import spa_shell

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.api_urls")),
    path("api/cafe/", include("cafe.api_urls")),
    path("api/cowork/", include("cowork.api_urls")),
    path("app/", spa_shell, name="spa_shell"),
    re_path(r"^app/(?P<path>.*)$", spa_shell, name="spa_shell_catchall"),
    path("login/", RedirectView.as_view(url="/app/account", permanent=False), name="legacy_login_redirect"),
    path("register/", RedirectView.as_view(url="/app/account", permanent=False), name="legacy_register_redirect"),
    path("profile/", RedirectView.as_view(url="/app/account", permanent=False), name="legacy_profile_redirect"),
    re_path(r"^cafe(?:/.*)?$", RedirectView.as_view(url="/app/cafe", permanent=False), name="legacy_cafe_redirect"),
    re_path(r"^cowork(?:/.*)?$", RedirectView.as_view(url="/app/cowork", permanent=False), name="legacy_cowork_redirect"),
    # Legacy cafe/cowork surfaces are intentionally disabled after cutover.
    re_path(r"^legacy/cafe(?:/.*)?$", RedirectView.as_view(url="/app/cafe", permanent=False), name="legacy_cafe_hard_redirect"),
    re_path(r"^legacy/cowork(?:/.*)?$", RedirectView.as_view(url="/app/cowork", permanent=False), name="legacy_cowork_hard_redirect"),
    path("legacy/", include("config.legacy_urls")),
    path("", spa_shell, name="spa_root"),
    re_path(r"^(?P<path>(?!admin/|api/|app/|legacy/|media/|static/).*)$", spa_shell, name="spa_root_catchall"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
