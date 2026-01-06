from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Booking, Space

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_type', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'}),
            'booking_type': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        
        if start and end and start >= end:
            raise forms.ValidationError(_("End time must be after start time."))
        return cleaned_data