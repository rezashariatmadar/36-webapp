from django.db import models
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time
from decimal import Decimal

class PricingPlan(models.Model):
    name = models.CharField(_("Plan Name"), max_length=100)
    daily_rate = models.DecimalField(_("Daily Rate"), max_digits=12, decimal_places=0, default=0, blank=True, null=True)
    hourly_rate = models.DecimalField(_("Hourly Rate"), max_digits=12, decimal_places=0, default=0, blank=True, null=True)
    monthly_rate = models.DecimalField(_("Monthly Rate"), max_digits=12, decimal_places=0, default=0, blank=True, null=True)
    six_month_rate = models.DecimalField(_("6-Month Rate"), max_digits=12, decimal_places=0, default=0, blank=True, null=True)
    yearly_rate = models.DecimalField(_("Yearly Rate"), max_digits=12, decimal_places=0, default=0, blank=True, null=True)
    
    is_contact_for_price = models.BooleanField(_("Contact for Price"), default=False)

    def __str__(self):
        return self.name

class Space(models.Model):
    class ZoneType(models.TextChoices):
        LONG_TABLE = 'LONG_TABLE', _('میز اشتراکی طولانی')
        DESK = 'DESK', _('میز شخصی (تکی)')
        SHARED_DESK = 'SHARED_DESK', _('میز اشتراکی (۴ نفره)')
        PRIVATE_ROOM_2 = 'PRIVATE_2', _('اتاق VIP (۲ نفره)')
        PRIVATE_ROOM_3 = 'PRIVATE_3', _('اتاق VIP (۳ نفره)')
        MEETING_ROOM = 'MEETING_ROOM', _('اتاق جلسه')

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', _('Available')
        OCCUPIED = 'OCCUPIED', _('Occupied')
        UNAVAILABLE = 'UNAVAILABLE', _('Unavailable')

    name = models.CharField(_("Space Name"), max_length=50, unique=True)
    zone = models.CharField(_("Zone Type"), max_length=20, choices=ZoneType.choices)
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    capacity = models.PositiveIntegerField(_("Capacity"), default=1)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Pricing Plan"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    # Nested Hierarchy
    parent_table = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='seats', verbose_name=_("Parent Table"))
    
    grid_row = models.IntegerField(_("Grid Row"), default=0)
    grid_col = models.IntegerField(_("Grid Col"), default=0)

    x_pos = models.FloatField(_("X Position (%)"), default=0.0, help_text="Horizontal position (0-100%)")
    y_pos = models.FloatField(_("Y Position (%)"), default=0.0, help_text="Vertical position (0-100%)")

    sort_order = models.PositiveIntegerField(_("Sort Order"), default=0)

    class Meta:
        verbose_name = _("Space")
        verbose_name_plural = _("Spaces")
        ordering = ['zone', 'sort_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_zone_display()})"

    def refresh_status(self):
        """Updates the status based on current active bookings."""
        if self.status == self.Status.UNAVAILABLE:
            return # Keep manual unavailable status
            
        now = timezone.now().date()
        active_booking = self.bookings.filter(
            status=Booking.Status.CONFIRMED,
            start_time__lte=now,
            end_time__gte=now
        ).exists()
        
        if active_booking:
            self.status = self.Status.OCCUPIED
        else:
            self.status = self.Status.AVAILABLE
        self.save()

    @property
    def is_nested(self):
        """Returns True if this zone should use the nested accordion UI."""
        return self.zone in [
            self.ZoneType.SHARED_DESK,
            self.ZoneType.PRIVATE_ROOM_2,
            self.ZoneType.PRIVATE_ROOM_3
        ]

class Booking(models.Model):
    class BookingType(models.TextChoices):
        HOURLY = 'HOURLY', _('Hourly')
        DAILY = 'DAILY', _('Daily')
        MONTHLY = 'MONTHLY', _('Monthly')
        SIX_MONTH = 'SIX_MONTH', _('6-Month')
        YEARLY = 'YEARLY', _('Yearly')

    class Status(models.TextChoices):
        PENDING_PAYMENT = 'PENDING', _('Pending Payment')
        CONFIRMED = 'CONFIRMED', _('Confirmed (Paid)')
        CANCELLED = 'CANCELLED', _('Cancelled')
        REFUNDED = 'REFUNDED', _('Refunded')
        COMPLETED = 'COMPLETED', _('Completed')

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name=_("User"))
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Space"))
    booking_type = models.CharField(_("Booking Type"), max_length=15, choices=BookingType.choices)
    
    start_time = jmodels.jDateField(_("Start Time"))
    end_time = jmodels.jDateField(_("End Time"))
    
    status = models.CharField(_("Status"), max_length=10, choices=Status.choices, default=Status.PENDING_PAYMENT)
    price_charged = models.DecimalField(_("Price Charged"), max_digits=12, decimal_places=0, default=0)
    settled_at = jmodels.jDateTimeField(_("Settled At"), null=True, blank=True)
    
    # Payment Tracking
    payment_token = models.CharField(_("Payment Token"), max_length=100, blank=True, null=True)
    transaction_id = models.CharField(_("Transaction ID"), max_length=100, blank=True, null=True)
    
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user} - {self.space} ({self.start_time})"

    @property
    def start_time_jalali(self):
        if not self.start_time: return ""
        return self.start_time.strftime("%Y/%m/%d")

    @property
    def end_time_jalali(self):
        if not self.end_time: return ""
        return self.end_time.strftime("%Y/%m/%d")

    def calculate_price(self):
        """Calculates the price based on booking type and pricing plan."""
        if not self.space or not self.space.pricing_plan:
            return 0
            
        plan = self.space.pricing_plan
        if plan.is_contact_for_price:
            return 0
            
        price = 0
        if self.booking_type == self.BookingType.HOURLY:
            price = plan.hourly_rate or 0
        elif self.booking_type == self.BookingType.DAILY:
            price = plan.daily_rate or 0
        elif self.booking_type == self.BookingType.MONTHLY:
            price = plan.monthly_rate or 0
        elif self.booking_type == self.BookingType.SIX_MONTH:
            price = plan.six_month_rate or 0
        elif self.booking_type == self.BookingType.YEARLY:
            price = plan.yearly_rate or 0
            
        return price

    def clean(self):
        # 1. Check Operating Hours (8 AM to 8 PM) - ONLY for HOURLY
        # Note: with DateField, we can't check 'time', so we skip for now
        # or assume the user is booking the 'day'.
        pass

        # 2. Logic Check for Long Table (Daily Only)
        if self.space and self.space.zone == Space.ZoneType.LONG_TABLE:
            if self.booking_type != self.BookingType.DAILY:
                raise ValidationError(_("The Long Table is only available for Daily reservations."))

        # 3. Logic Check for Shared Desk (Monthly Only)
        if self.space and self.space.zone == Space.ZoneType.SHARED_DESK:
            if self.booking_type != self.BookingType.MONTHLY:
                raise ValidationError(_("Shared Tables are only available for Monthly reservations."))

        # 4. Logic Check for Private Rooms (Monthly, 6-Month, or Yearly)
        if self.space and self.space.zone in [Space.ZoneType.PRIVATE_ROOM_2, Space.ZoneType.PRIVATE_ROOM_3]:
            allowed_types = [self.BookingType.MONTHLY, self.BookingType.SIX_MONTH, self.BookingType.YEARLY]
            if self.booking_type not in allowed_types:
                raise ValidationError(_("This space is only available for Monthly, 6-Month, or Yearly reservations."))

        # 5. Standard Conflict Check
        if self.start_time and self.end_time:
            if self.start_time > self.end_time:
                raise ValidationError(_("End time must be after start time."))
            
            overlapping = Booking.objects.filter(
                space=self.space,
                status=self.Status.CONFIRMED,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)
            
            if overlapping.exists():
                raise ValidationError(_("This space is already booked for the selected time."))
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_refundable(self):
        """Refund policy: 12 hours after reservation creation."""
        now = timezone.now()
        diff = now - self.created_at
        return diff.total_seconds() < (12 * 3600)
