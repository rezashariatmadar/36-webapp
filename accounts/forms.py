from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .forms_mixins import DigitNormalizationMixin

class UserRegistrationForm(DigitNormalizationMixin, forms.ModelForm):
    normalize_fields = ['phone_number', 'national_id']
    
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'input-standard'})
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password'), 'class': 'input-standard'})
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'national_id', 'full_name')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': '09xxxxxxxxx'}),
            'national_id': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'کد ملی ۱۰ رقمی'}),
            'full_name': forms.TextInput(attrs={'class': 'input-standard', 'placeholder': 'نام و نام خانوادگی'}),
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

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(DigitNormalizationMixin, AuthenticationForm):
    normalize_fields = ['username']
    
    username = forms.CharField(
        label=_("Phone Number"), 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': '09xxxxxxxxx', 'class': 'input-standard'})
    )
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': '******', 'class': 'input-standard'})
    )