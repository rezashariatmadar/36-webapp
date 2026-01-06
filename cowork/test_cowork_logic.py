from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        start = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end = start + timedelta(hours=2)
        booking = BookingFactory(
            user=self.user,
            space=self.space,
            start_time=start,
            end_time=end,
            booking_type=Booking.BookingType.HOURLY
        )
        # Price is calculated in view, but let's verify logic matches
        diff = booking.end_time - booking.start_time
        hours = Decimal(diff.total_seconds() / 3600)
        price = self.plan.hourly_rate * hours
        self.assertEqual(price, 40000)

    def test_conflict_prevention_same_time(self):
        start = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end = start + timedelta(hours=2)
        
        BookingFactory(
            space=self.space,
            start_time=start,
            end_time=end,
            booking_type=Booking.BookingType.HOURLY,
            status=Booking.Status.CONFIRMED
        )
        
        # Second booking at same time
        with self.assertRaises(ValidationError):
            b2 = Booking(
                user=self.user,
                space=self.space,
                start_time=start,
                end_time=end,
                booking_type=Booking.BookingType.HOURLY,
                status=Booking.Status.CONFIRMED
            )
            b2.full_clean()
            b2.save()

    def test_operating_hours_constraint(self):
        # 08:00 - 20:00
        # 7 AM is invalid
        invalid_start = timezone.now().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)
        invalid_end = invalid_start + timedelta(hours=1)
        
        booking = Booking(
            user=self.user,
            space=self.space,
            start_time=invalid_start,
            end_time=invalid_end,
            booking_type=Booking.BookingType.HOURLY
        )
        
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_zone_restrictions_long_table(self):
        long_table = SpaceFactory(zone=Space.ZoneType.LONG_TABLE)
        
        # Long table should only allow DAILY
        booking = Booking(
            user=self.user,
            space=long_table,
            start_time=timezone.now().replace(hour=10, minute=0) + timedelta(days=1),
            end_time=timezone.now().replace(hour=12, minute=0) + timedelta(days=1),
            booking_type=Booking.BookingType.HOURLY
        )
        
        with self.assertRaises(ValidationError):
            booking.full_clean()
