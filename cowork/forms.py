from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Booking, Space
from datetime import timedelta
from django.utils import timezone
import jdatetime
from django_jalali import forms as jforms
from accounts.forms_mixins import DigitNormalizationMixin

class BookingForm(DigitNormalizationMixin, forms.ModelForm):
    normalize_fields = ['start_time']
    
    # Use django-jalali form fields for automatic validation and conversion
    start_time = jforms.jDateField(
        label=_("Start Date"),
        widget=forms.TextInput(attrs={'class': 'jalali-date input-standard', 'autocomplete': 'off'})
    )
    end_time = jforms.jDateField(
        label=_("End Date"),
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Booking
        fields = ['booking_type', 'start_time', 'end_time']
        widgets = {
            'booking_type': forms.Select(attrs={'class': 'select select-bordered w-full bg-white/5 border-white/10 text-white rounded-2xl'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.space = kwargs.pop('space', None)
        super().__init__(*args, **kwargs)
        
        if self.space:
            self.instance.space = self.space
            
            # Zone-specific field customization
            if self.space.zone == Space.ZoneType.LONG_TABLE:
                self.fields['booking_type'].initial = Booking.BookingType.DAILY
                self.fields['booking_type'].widget = forms.HiddenInput()
                
            elif self.space.zone == Space.ZoneType.DESK:
                self.fields['booking_type'].choices = [
                    (Booking.BookingType.DAILY, _('Daily')),
                    (Booking.BookingType.MONTHLY, _('Monthly')),
                ]
                
            elif self.space.zone in [Space.ZoneType.SHARED_DESK, Space.ZoneType.PRIVATE_ROOM_2, Space.ZoneType.PRIVATE_ROOM_3]:
                # Shared Table is Monthly ONLY
                if self.space.zone == Space.ZoneType.SHARED_DESK:
                    self.fields['booking_type'].initial = Booking.BookingType.MONTHLY
                    self.fields['booking_type'].widget = forms.HiddenInput()
                else:
                    # VIP has choices
                    self.fields['booking_type'].choices = [
                        (Booking.BookingType.MONTHLY, _('Monthly')),
                        (Booking.BookingType.SIX_MONTH, _('6-Month')),
                        (Booking.BookingType.YEARLY, _('Yearly')),
                    ]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_time') # Now a jdatetime.date object
        booking_type = cleaned_data.get('booking_type')
        
        # Auto-calculate end date if needed
        if start_date:
            if booking_type == Booking.BookingType.DAILY:
                # Same day or next day? User said "just the date they are reserving" 
                # implying start=end for single day.
                # However, calculate_price expects diff.days >= 1 for Daily? 
                # Let's use start_date + 1 day for Daily to be safe and logical.
                cleaned_data['end_time'] = start_date + timedelta(days=1)
            elif booking_type == Booking.BookingType.MONTHLY:
                cleaned_data['end_time'] = start_date + timedelta(days=30)
            elif booking_type == Booking.BookingType.SIX_MONTH:
                cleaned_data['end_time'] = start_date + timedelta(days=180)
            elif booking_type == Booking.BookingType.YEARLY:
                cleaned_data['end_time'] = start_date + timedelta(days=365)
            
            end_date = cleaned_data['end_time']
            
            # Update the form instance end_time so it's available for preview
            self.instance.end_time = end_date
            
            if start_date > end_date:
                raise forms.ValidationError(_("End time must be after start time."))
        
        return cleaned_data