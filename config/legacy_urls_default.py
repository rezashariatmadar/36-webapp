from django.urls import include, path

urlpatterns = [
    path('', include(('accounts.urls', 'legacy_accounts'), namespace='legacy_accounts')),
    path('cafe/', include(('cafe.urls', 'legacy_cafe'), namespace='legacy_cafe')),
    path('cowork/', include(('cowork.urls', 'legacy_cowork'), namespace='legacy_cowork')),
]
