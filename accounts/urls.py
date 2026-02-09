from django.urls import path
from .views import (
    LogoutView,
    admin_user_list, toggle_user_status, change_user_role, UserListAPI
)

app_name = 'accounts'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Admin Views
    path('staff/users/', admin_user_list, name='user_list'),
    path('staff/users/toggle/<int:user_id>/', toggle_user_status, name='toggle_user_status'),
    path('staff/users/role/<int:user_id>/<str:new_role>/', change_user_role, name='change_user_role'),
    
    # API
    path('api/users/', UserListAPI.as_view(), name='api_user_list'),
]
