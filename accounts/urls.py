from django.urls import path
from .views import (
    RegisterView, CustomLoginView, LogoutView, home_view, 
    admin_user_list, toggle_user_status, change_user_role, UserListAPI, profile_view
)

app_name = 'accounts'

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    
    # Admin Views
    path('admin/users/', admin_user_list, name='user_list'),
    path('admin/users/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('admin/users/role/<int:user_id>/<str:new_role>/', change_user_role, name='change_user_role'),
    
    # API
    path('api/users/', UserListAPI.as_view(), name='api_user_list'),
]
