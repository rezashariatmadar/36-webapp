from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms_mixins import DigitNormalizationMixin
import jdatetime

class UserRegistrationForm(DigitNormalizationMixin, forms.ModelForm):
    normalize_fields = ['phone_number', 'national_id']
    
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'input-standard', 'autocomplete': 'new-password'})
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password'), 'class': 'input-standard', 'autocomplete': 'new-password'})
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'national_id', 'full_name')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': '09xxxxxxxxx', 'autocomplete': 'tel'}),
            'national_id': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'کد ملی ۱۰ رقمی', 'autocomplete': 'off'}),
            'full_name': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'نام و نام خانوادگی', 'autocomplete': 'name'}),
        }

    def clean_confirm_password(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("confirm_password")
        if p1 != p2: raise forms.ValidationError(_("Passwords don't match"))
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit: user.save()
        return user

class ProfileForm(DigitNormalizationMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'birth_date')
        widgets = {
            'birth_date': forms.TextInput(attrs={'class': 'input-standard jalali-date', 'placeholder': '----/--/--'}),
            'full_name': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'نام و نام خانوادگی'}),
        }

    def clean_birth_date(self):
        value = self.cleaned_data.get('birth_date')
        if not value:
            return value

        if isinstance(value, str):
            try:
                parts = [int(p) for p in value.replace('-', '/').split('/') if p]
                if len(parts) != 3:
                    raise ValueError
                value = jdatetime.date(parts[0], parts[1], parts[2])
            except Exception:
                raise forms.ValidationError(_("Invalid birth date format. Use YYYY/MM/DD."))
        return value

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(DigitNormalizationMixin, AuthenticationForm):
    normalize_fields = ['username']
    
    username = forms.CharField(
        label=_("Phone Number"), 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': '09xxxxxxxxx', 'class': 'input-standard', 'autocomplete': 'username'})
    )
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': '******', 'class': 'input-standard', 'autocomplete': 'current-password'})
    )
