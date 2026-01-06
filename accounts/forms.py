from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
        help_text=_("Use your National ID as your initial password.")
    )
    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password')})
    )

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'national_id', 'full_name')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '09xxxxxxxxx'}),
            'national_id': forms.TextInput(attrs={'placeholder': '0012345678'}),
            'full_name': forms.TextInput(attrs={'placeholder': _('Full Name')}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Passwords don't match"))
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Phone Number"),
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': '09xxxxxxxxx'})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': '******'}),
    )
