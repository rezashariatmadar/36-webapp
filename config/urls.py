from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .seo_views import robots_txt, sitemap_xml

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.api_urls')),
    path('api/freelancers/', include('accounts.freelancer_api_urls')),
    path('api/blog/', include('blog.api_urls')),
    path('api/cafe/', include('cafe.api_urls')),
    path('api/cowork/', include('cowork.api_urls')),
    path('api/staff/', include('accounts.staff_api_urls')),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
