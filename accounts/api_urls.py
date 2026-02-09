from django.urls import path

from .api_views import (
    SessionCsrfAPIView,
    SessionLoginAPIView,
    SessionLogoutAPIView,
    SessionMeAPIView,
    SessionProfileAPIView,
    SessionRegisterAPIView,
    StaffUserListAPIView,
    StaffUserRoleAPIView,
    StaffUserStatusAPIView,
)

app_name = "accounts_api"

urlpatterns = [
    path("csrf/", SessionCsrfAPIView.as_view(), name="csrf"),
    path("login/", SessionLoginAPIView.as_view(), name="login"),
    path("logout/", SessionLogoutAPIView.as_view(), name="logout"),
    path("register/", SessionRegisterAPIView.as_view(), name="register"),
    path("me/", SessionMeAPIView.as_view(), name="me"),
    path("profile/", SessionProfileAPIView.as_view(), name="profile"),
    path("staff/users/", StaffUserListAPIView.as_view(), name="staff_users"),
    path("staff/users/<int:user_id>/status/", StaffUserStatusAPIView.as_view(), name="staff_user_status"),
    path("staff/users/<int:user_id>/role/", StaffUserRoleAPIView.as_view(), name="staff_user_role"),
]
