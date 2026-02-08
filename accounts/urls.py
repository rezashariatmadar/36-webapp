from django.urls import path
from django.views.generic import RedirectView
from .views import (
    LogoutView,
    admin_user_list, toggle_user_status, change_user_role, UserListAPI
)

app_name = 'accounts'

urlpatterns = [
    path('', RedirectView.as_view(url='/app', permanent=False), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Admin Views
    path('admin/users/', admin_user_list, name='user_list'),
    path('admin/users/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('admin/users/role/<int:user_id>/<str:new_role>/', change_user_role, name='change_user_role'),
    
    # API
    path('api/users/', UserListAPI.as_view(), name='api_user_list'),
]
