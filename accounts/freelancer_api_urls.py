from django.urls import path

from .freelancer_api_views import (
    PublicFreelancerDetailAPIView,
    PublicFreelancerFlairsAPIView,
    PublicFreelancersAPIView,
    PublicFreelancerSpecialtiesAPIView,
)

app_name = "freelancers_api"

urlpatterns = [
    path("specialties/", PublicFreelancerSpecialtiesAPIView.as_view(), name="specialties"),
    path("flairs/", PublicFreelancerFlairsAPIView.as_view(), name="flairs"),
    path("", PublicFreelancersAPIView.as_view(), name="list"),
    path("<slug:slug>/", PublicFreelancerDetailAPIView.as_view(), name="detail"),
]
