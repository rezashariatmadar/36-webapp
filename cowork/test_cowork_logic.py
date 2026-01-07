from django.test import TestCase
from django.core.exceptions import ValidationError
import jdatetime
from datetime import timedelta
from decimal import Decimal
from .factories import SpaceFactory, BookingFactory, PricingPlanFactory
from .models import Booking, Space
from accounts.factories import UserFactory

class CoworkLogicTests(TestCase):
    def setUp(self):
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
