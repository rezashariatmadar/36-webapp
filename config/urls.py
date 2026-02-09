from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from theme.views import spa_shell

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("api/auth/", include("accounts.api_urls")),
    path("api/cafe/", include("cafe.api_urls")),
    path("api/cowork/", include("cowork.api_urls")),
    path("app/", spa_shell, name="spa_shell"),
    re_path(r"^app/(?P<path>.*)$", spa_shell, name="spa_shell_catchall"),
    path("", spa_shell, name="spa_root"),
    re_path(
        r"^(?P<path>(?!(admin/|api/|app/|legacy/|media/|static/|login(?:/|$)|register(?:/|$)|profile(?:/|$)|cafe(?:/|$)|cowork(?:/|$))).*)$",
        spa_shell,
        name="spa_root_catchall",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
