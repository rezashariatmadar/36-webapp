import jdatetime
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.factories import UserFactory
from cowork.factories import SpaceFactory
from cowork.models import Booking


class CoworkSPAApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.space = SpaceFactory()
        self.start_date = jdatetime.date.today().strftime("%Y-%m-%d")

    def test_spaces_endpoint_returns_zone_payload(self):
        response = self.client.get("/api/cowork/spaces/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("zones", response.data)

    def test_preview_endpoint_returns_price(self):
        response = self.client.get(
            "/api/cowork/bookings/preview/",
            {
                "space_id": self.space.id,
                "booking_type": Booking.BookingType.DAILY,
                "start_time": self.start_date,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["valid"])
        self.assertIn("price", response.data)

    def test_preview_requires_space_id_and_valid_payload(self):
        missing_space = self.client.get("/api/cowork/bookings/preview/")
        self.assertEqual(missing_space.status_code, 400)

        invalid_payload = self.client.get(
            "/api/cowork/bookings/preview/",
            {"space_id": self.space.id, "booking_type": Booking.BookingType.DAILY, "start_time": "invalid"},
        )
        self.assertEqual(invalid_payload.status_code, 400)

    def test_create_booking_requires_authentication(self):
        response = self.client.post(
            "/api/cowork/bookings/",
            {
                "space_id": self.space.id,
                "booking_type": Booking.BookingType.DAILY,
                "start_time": self.start_date,
            },
            format="json",
        )
        self.assertIn(response.status_code, [401, 403])

    def test_create_booking_validates_required_fields(self):
        self.client.force_authenticate(user=self.user)
        missing_space = self.client.post(
            "/api/cowork/bookings/",
            {"booking_type": Booking.BookingType.DAILY, "start_time": self.start_date},
            format="json",
        )
        self.assertEqual(missing_space.status_code, 400)

        invalid_payload = self.client.post(
            "/api/cowork/bookings/",
            {"space_id": self.space.id, "booking_type": Booking.BookingType.DAILY, "start_time": "bad-date"},
            format="json",
        )
        self.assertEqual(invalid_payload.status_code, 400)

    def test_create_booking_and_list_my_bookings(self):
        self.client.force_authenticate(user=self.user)
        create_response = self.client.post(
            "/api/cowork/bookings/",
            {
                "space_id": self.space.id,
                "booking_type": Booking.BookingType.DAILY,
                "start_time": self.start_date,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

        list_response = self.client.get("/api/cowork/my-bookings/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data["bookings"]), 1)

    def test_my_bookings_requires_authentication(self):
        response = self.client.get("/api/cowork/my-bookings/")
        self.assertIn(response.status_code, [401, 403])
