from django.test import TestCase
import jdatetime
from datetime import timedelta
from .forms import BookingForm
from .models import Booking, Space, PricingPlan
from .factories import SpaceFactory, PricingPlanFactory

class BookingFormTests(TestCase):
    def setUp(self):
        self.plan = PricingPlanFactory()
        
    def test_communal_table_defaults(self):
        space = SpaceFactory(zone=Space.ZoneType.LONG_TABLE, pricing_plan=self.plan)
        form = BookingForm(space=space)
        
        # Check initial values
        self.assertEqual(form.fields['booking_type'].initial, Booking.BookingType.DAILY)
        
        # Check hidden widgets
        self.assertTrue(form.fields['booking_type'].widget.is_hidden)
        self.assertTrue(form.fields['end_time'].widget.is_hidden)
        
        # Submit form with Jalali date string
        start = jdatetime.date.today() + timedelta(days=1)
        data = {
            'booking_type': Booking.BookingType.DAILY,
            'start_time': start.strftime('%Y-%m-%d'),
        }
        form = BookingForm(data=data, space=space)
        self.assertTrue(form.is_valid(), form.errors)
        
        # Check auto-calculated end time
        self.assertEqual(form.cleaned_data['end_time'], start + timedelta(days=1))

    def test_shared_desk_monthly_only(self):
        space = SpaceFactory(zone=Space.ZoneType.SHARED_DESK, pricing_plan=self.plan)
        form = BookingForm(space=space)
        
        self.assertEqual(form.fields['booking_type'].initial, Booking.BookingType.MONTHLY)
        self.assertTrue(form.fields['booking_type'].widget.is_hidden)
        
        start = jdatetime.date.today() + timedelta(days=1)
        data = {
            'booking_type': Booking.BookingType.MONTHLY,
            'start_time': start.strftime('%Y-%m-%d'),
        }
        form = BookingForm(data=data, space=space)
        self.assertTrue(form.is_valid(), form.errors)
        
        # Check auto-calculated end time (30 days)
        self.assertEqual(form.cleaned_data['end_time'], start + timedelta(days=30))

    def test_vip_6_month_calculation(self):
        space = SpaceFactory(zone=Space.ZoneType.PRIVATE_ROOM_2, pricing_plan=self.plan)
        start = jdatetime.date.today() + timedelta(days=1)
        data = {
            'booking_type': Booking.BookingType.SIX_MONTH,
            'start_time': start.strftime('%Y-%m-%d'),
        }
        form = BookingForm(data=data, space=space)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['end_time'], start + timedelta(days=180))

    def test_individual_desk_choices(self):
        space = SpaceFactory(zone=Space.ZoneType.DESK, pricing_plan=self.plan)
        form = BookingForm(space=space)
        
        choices = [c[0] for c in form.fields['booking_type'].choices]
        self.assertIn(Booking.BookingType.DAILY, choices)
        self.assertIn(Booking.BookingType.MONTHLY, choices)
        self.assertNotIn(Booking.BookingType.HOURLY, choices)
