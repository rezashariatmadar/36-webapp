from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time

class PricingPlan(models.Model):
    name = models.CharField(_("Plan Name"), max_length=100)
    daily_rate = models.DecimalField(_("Daily Rate"), max_digits=12, decimal_places=0, default=0)
    hourly_rate = models.DecimalField(_("Hourly Rate"), max_digits=12, decimal_places=0, default=0)
    monthly_rate = models.DecimalField(_("Monthly Rate"), max_digits=12, decimal_places=0, default=0)
    six_month_rate = models.DecimalField(_("6-Month Rate"), max_digits=12, decimal_places=0, default=0)
    yearly_rate = models.DecimalField(_("Yearly Rate"), max_digits=12, decimal_places=0, default=0)
    
    is_contact_for_price = models.BooleanField(_("Contact for Price"), default=False)

    def __str__(self):
        return self.name

class Space(models.Model):
    class ZoneType(models.TextChoices):
        LONG_TABLE = 'LONG_TABLE', _('Communal Long Table')
        DESK = 'DESK', _('Individual Desk')
        PRIVATE_ROOM = 'PRIVATE_ROOM', _('Private Room')
        MEETING_ROOM = 'MEETING_ROOM', _('Meeting Room')

    name = models.CharField(_("Space Name"), max_length=50, unique=True)
    zone = models.CharField(_("Zone Type"), max_length=20, choices=ZoneType.choices)
    capacity = models.PositiveIntegerField(_("Capacity"), default=1)
    pricing_plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True, verbose_name=_("Pricing Plan"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    grid_row = models.IntegerField(_("Grid Row"), default=0)
    grid_col = models.IntegerField(_("Grid Col"), default=0)

    class Meta:
        verbose_name = _("Space")
        verbose_name_plural = _("Spaces")
        ordering = ['zone', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_zone_display()})"

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
    
    start_time = models.DateTimeField(_("Start Time"))
    end_time = models.DateTimeField(_("End Time"))
    
    status = models.CharField(_("Status"), max_length=10, choices=Status.choices, default=Status.PENDING_PAYMENT)
    price_charged = models.DecimalField(_("Price Charged"), max_digits=12, decimal_places=0, default=0)
    
    # Payment Tracking
    payment_token = models.CharField(_("Payment Token"), max_length=100, blank=True, null=True)
    transaction_id = models.CharField(_("Transaction ID"), max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user} - {self.space} ({self.start_time.date()})"

    def clean(self):
        # 1. Check Operating Hours (8 AM to 8 PM)
        # Note: We check the time part of start/end
        opening_time = time(8, 0)
        closing_time = time(20, 0)
        
        if self.start_time and (self.start_time.time() < opening_time or self.start_time.time() > closing_time):
            raise ValidationError(_("Reservations are only allowed between 08:00 and 20:00."))
        if self.end_time and (self.end_time.time() < opening_time or self.end_time.time() > closing_time):
            raise ValidationError(_("Reservations are only allowed between 08:00 and 20:00."))

        # 2. Logic Check for Long Table (Daily Only)
        if self.space and self.space.zone == Space.ZoneType.LONG_TABLE:
            if self.booking_type != self.BookingType.DAILY:
                raise ValidationError(_("The Long Table is only available for Daily reservations."))

        # 3. Standard Conflict Check
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
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
