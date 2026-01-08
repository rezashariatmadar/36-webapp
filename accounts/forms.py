from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

GLASS_INPUT_CLASSES = 'bg-white/5 border-white/10 text-white placeholder-white/50 focus:bg-white/10 focus:border-accent input input-bordered w-full'

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': GLASS_INPUT_CLASSES})
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password'), 'class': GLASS_INPUT_CLASSES})
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'national_id', 'full_name')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': GLASS_INPUT_CLASSES, 'placeholder': '09xxxxxxxxx'}),
            'national_id': forms.TextInput(attrs={'class': GLASS_INPUT_CLASSES, 'placeholder': '10-digit National ID'}),
            'full_name': forms.TextInput(attrs={'class': GLASS_INPUT_CLASSES, 'placeholder': 'Full Name'}),
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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': GLASS_INPUT_CLASSES}),
            'full_name': forms.TextInput(attrs={'class': GLASS_INPUT_CLASSES}),
        }

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Phone Number"), 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': '09xxxxxxxxx', 'class': GLASS_INPUT_CLASSES})
    )
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'placeholder': '******', 'class': GLASS_INPUT_CLASSES})
    )