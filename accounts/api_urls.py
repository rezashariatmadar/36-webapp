from django.urls import path

from .api_views import (
    SessionLoginAPIView,
    SessionLogoutAPIView,
    SessionMeAPIView,
    SessionProfileAPIView,
    SessionRegisterAPIView,
)

app_name = "accounts_api"

urlpatterns = [
    path("login/", SessionLoginAPIView.as_view(), name="login"),
    path("logout/", SessionLogoutAPIView.as_view(), name="logout"),
    path("register/", SessionRegisterAPIView.as_view(), name="register"),
    path("me/", SessionMeAPIView.as_view(), name="me"),
    path("profile/", SessionProfileAPIView.as_view(), name="profile"),
]
