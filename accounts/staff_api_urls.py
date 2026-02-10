from django.urls import path

from .staff_api_views import (
    StaffAnalyticsOverviewAPIView,
    StaffUserRoleAPIView,
    StaffUserStatusAPIView,
    StaffUsersAPIView,
)

app_name = "staff_api"

urlpatterns = [
    path("analytics/overview/", StaffAnalyticsOverviewAPIView.as_view(), name="analytics_overview"),
    path("users/", StaffUsersAPIView.as_view(), name="users"),
    path("users/<int:user_id>/status/", StaffUserStatusAPIView.as_view(), name="user_status"),
    path("users/<int:user_id>/role/", StaffUserRoleAPIView.as_view(), name="user_role"),
]

