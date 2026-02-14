from django.urls import path

from .api_views import (
    SessionLoginAPIView,
    SessionLogoutAPIView,
    SessionMeAPIView,
    SessionProfileAPIView,
    SessionRegisterAPIView,
)
from .freelancer_api_views import (
    OwnerFreelancerFlairsAPIView,
    OwnerFreelancerProfileAPIView,
    OwnerFreelancerServiceDetailAPIView,
    OwnerFreelancerServicesAPIView,
    OwnerFreelancerSpecialtiesAPIView,
    OwnerFreelancerSubmitAPIView,
)

app_name = "accounts_api"

urlpatterns = [
    path("login/", SessionLoginAPIView.as_view(), name="login"),
    path("logout/", SessionLogoutAPIView.as_view(), name="logout"),
    path("register/", SessionRegisterAPIView.as_view(), name="register"),
    path("me/", SessionMeAPIView.as_view(), name="me"),
    path("profile/", SessionProfileAPIView.as_view(), name="profile"),
    path("freelancer-profile/", OwnerFreelancerProfileAPIView.as_view(), name="freelancer_profile"),
    path("freelancer-profile/submit/", OwnerFreelancerSubmitAPIView.as_view(), name="freelancer_profile_submit"),
    path("freelancer-specialties/", OwnerFreelancerSpecialtiesAPIView.as_view(), name="freelancer_specialties"),
    path("freelancer-flairs/", OwnerFreelancerFlairsAPIView.as_view(), name="freelancer_flairs"),
    path("freelancer-services/", OwnerFreelancerServicesAPIView.as_view(), name="freelancer_services"),
    path("freelancer-services/<int:service_id>/", OwnerFreelancerServiceDetailAPIView.as_view(), name="freelancer_service_detail"),
]
