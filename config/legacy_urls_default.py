from django.urls import include, path

urlpatterns = [
    path('', include(('accounts.urls', 'legacy_accounts'), namespace='legacy_accounts')),
    path('cafe/', include(('cafe.urls', 'cafe'), namespace='cafe')),
    path('cowork/', include(('cowork.urls', 'cowork'), namespace='cowork')),
]
