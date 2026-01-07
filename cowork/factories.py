import factory
from factory.django import DjangoModelFactory
from cowork.models import Space, Booking, PricingPlan
from accounts.factories import UserFactory
import jdatetime
from datetime import timedelta

class PricingPlanFactory(DjangoModelFactory):
    class Meta:
        model = PricingPlan

    name = factory.Sequence(lambda n: f'Plan {n}')
    hourly_rate = 20000
    daily_rate = 150000
    monthly_rate = 3000000

class SpaceFactory(DjangoModelFactory):
    class Meta:
        model = Space

    name = factory.Sequence(lambda n: f'Space {n}')
    zone = Space.ZoneType.DESK
    pricing_plan = factory.SubFactory(PricingPlanFactory)
    capacity = 1
    is_active = True

class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    space = factory.SubFactory(SpaceFactory)
    start_time = factory.LazyFunction(jdatetime.date.today)
    end_time = factory.LazyAttribute(lambda o: o.start_time + timedelta(days=1))
    booking_type = Booking.BookingType.HOURLY
    status = Booking.Status.CONFIRMED
