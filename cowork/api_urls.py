from django.urls import path

from .api_views import (
    CoworkBookingPreviewAPIView,
    CoworkBookingsAPIView,
    CoworkMyBookingsAPIView,
    CoworkSpacesAPIView,
)

app_name = "cowork_api"

urlpatterns = [
    path("spaces/", CoworkSpacesAPIView.as_view(), name="spaces"),
    path("bookings/preview/", CoworkBookingPreviewAPIView.as_view(), name="booking_preview"),
    path("bookings/", CoworkBookingsAPIView.as_view(), name="bookings"),
    path("my-bookings/", CoworkMyBookingsAPIView.as_view(), name="my_bookings"),
]
