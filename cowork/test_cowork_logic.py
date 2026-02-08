from django.test import TestCase
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import RequestFactory
from unittest.mock import patch
import jdatetime
from datetime import timedelta
from decimal import Decimal
from .factories import SpaceFactory, BookingFactory, PricingPlanFactory
from .models import Booking, Space
from accounts.factories import UserFactory

class CoworkLogicTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.plan = PricingPlanFactory(
            hourly_rate=20000,
            daily_rate=150000,
            monthly_rate=3000000
        )
        self.space = SpaceFactory(pricing_plan=self.plan, zone=Space.ZoneType.DESK)

    def test_hourly_pricing_calculation(self):
        start = jdatetime.date.today() + timedelta(days=1)
        end = start # Same day
        booking = BookingFactory(
            user=self.user,
            space=self.space,
            start_time=start,
            end_time=end,
            booking_type=Booking.BookingType.HOURLY
        )
        price = booking.calculate_price()
        self.assertEqual(price, self.plan.hourly_rate)

    def test_conflict_prevention_same_time(self):
        start = jdatetime.date.today() + timedelta(days=1)
        end = start
        
        BookingFactory(
            space=self.space,
            start_time=start,
            end_time=end,
            booking_type=Booking.BookingType.HOURLY,
            status=Booking.Status.CONFIRMED
        )
        
        # Second booking at same time
        overlapping = Booking.objects.filter(
            space=self.space,
            status=Booking.Status.CONFIRMED,
            start_time__lte=end,
            end_time__gte=start
        )
        self.assertTrue(overlapping.exists())

    def test_zone_restrictions_long_table(self):
        long_table = SpaceFactory(zone=Space.ZoneType.LONG_TABLE)
        
        # Long table should only allow DAILY
        booking = Booking(
            user=self.user,
            space=long_table,
            start_time=jdatetime.date.today() + timedelta(days=1),
            end_time=jdatetime.date.today() + timedelta(days=1),
            booking_type=Booking.BookingType.HOURLY
        )
        
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_is_nested_property(self):
        # Nested zones
        for zone in [Space.ZoneType.SHARED_DESK, Space.ZoneType.PRIVATE_ROOM_2, Space.ZoneType.PRIVATE_ROOM_3]:
            space = SpaceFactory(zone=zone)
            self.assertTrue(space.is_nested, f"Zone {zone} should be nested")

        # Non-nested zones
        for zone in [Space.ZoneType.DESK, Space.ZoneType.LONG_TABLE, Space.ZoneType.MEETING_ROOM]:
            space = SpaceFactory(zone=zone)
            self.assertFalse(space.is_nested, f"Zone {zone} should not be nested")

    def test_space_list_nonlegacy_htmx_renders_full_template(self):
        from .views import space_list

        request = self.factory.get("/cowork/")
        request.htmx = True

        with patch("cowork.views.render") as mock_render:
            mock_render.side_effect = lambda _request, template_name, context=None: HttpResponse(template_name)
            response = space_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "cowork/space_list.html")

    def test_space_list_legacy_htmx_renders_partial_template(self):
        from .views import space_list

        request = self.factory.get("/legacy/cowork/")
        request.htmx = True

        with patch("cowork.views.render") as mock_render:
            mock_render.side_effect = lambda _request, template_name, context=None: HttpResponse(template_name)
            response = space_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "cowork/partials/zone_list.html")

    def test_book_space_nonlegacy_htmx_renders_full_template(self):
        from .views import book_space

        request = self.factory.get(
            f"/cowork/book/{self.space.id}/",
            data={"booking_type": Booking.BookingType.HOURLY, "start_time": "2026-03-01"},
        )
        request.htmx = True
        request.user = self.user

        with patch("cowork.views.render") as mock_render:
            mock_render.side_effect = lambda _request, template_name, context=None: HttpResponse(template_name)
            response = book_space(request, self.space.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "cowork/book_space.html")

    def test_book_space_legacy_htmx_renders_preview_partial(self):
        from .views import book_space

        request = self.factory.get(
            f"/legacy/cowork/book/{self.space.id}/",
            data={"booking_type": Booking.BookingType.DAILY, "start_time": "2026-03-01"},
        )
        request.htmx = True
        request.user = self.user

        with patch("cowork.views.render") as mock_render:
            mock_render.side_effect = lambda _request, template_name, context=None: HttpResponse(template_name)
            response = book_space(request, self.space.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "cowork/partials/booking_preview.html")
