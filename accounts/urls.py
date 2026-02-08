from django.urls import path
from django.views.generic import RedirectView
from .views import (
    LogoutView, home_view,
    admin_user_list, toggle_user_status, change_user_role, UserListAPI
)

app_name = 'accounts'

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RedirectView.as_view(url='/app/account', permanent=False), name='register'),
    path('login/', RedirectView.as_view(url='/app/account', permanent=False), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', RedirectView.as_view(url='/app/account', permanent=False), name='profile'),
    
    # Admin Views
    path('admin/users/', admin_user_list, name='user_list'),
    path('admin/users/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('admin/users/role/<int:user_id>/<str:new_role>/', change_user_role, name='change_user_role'),
    
    # API
    path('api/users/', UserListAPI.as_view(), name='api_user_list'),
]
