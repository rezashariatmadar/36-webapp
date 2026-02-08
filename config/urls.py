from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from theme.views import spa_shell

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api_urls')),
    path('api/cafe/', include('cafe.api_urls')),
    path('api/cowork/', include('cowork.api_urls')),
    path('app/', spa_shell, name='spa_shell'),
    re_path(r'^app/(?P<path>.*)$', spa_shell, name='spa_shell_catchall'),
    path('', include('accounts.urls')),
    path('cafe/', include('cafe.urls')),
    path('cowork/', include('cowork.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
