from django.urls import include, path

urlpatterns = [
    path('', include('accounts.urls')),
    path('cafe/', include('cafe.urls')),
    path('cowork/', include('cowork.urls')),
]
