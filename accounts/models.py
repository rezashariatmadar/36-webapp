import re
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_iranian_national_id(national_id: str) -> bool:
    """Validates an Iranian National ID (Code Melli)."""
    if not re.match(r'^\d{10}$', national_id):
        return False
    check_digit = int(national_id[9])
    if len(set(national_id)) == 1:
        return False
    sum_digits = sum(int(national_id[i]) * (10 - i) for i in range(9))
    remainder = sum_digits % 11
    if remainder < 2:
        return check_digit == remainder
    else:
        return check_digit == (11 - remainder)

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)

def validate_national_id_field(value):
    if not validate_iranian_national_id(value):
        raise ValidationError(_('Invalid Iranian National ID.'))

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message=_("Phone number must be entered in the format: '09xxxxxxxxx'. Up to 11 digits allowed.")
    )
    phone_number = models.CharField(_('phone number'), validators=[phone_regex], max_length=15, unique=True)
    national_id = models.CharField(_('national ID'), max_length=10, blank=True, null=True, validators=[validate_national_id_field])
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    birth_date = jmodels.jDateField(_('birth date'), null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    @property
    def is_admin(self):
        return self.is_superuser or self.groups.filter(name='Admin').exists()

    @property
    def is_barista(self):
        return self.groups.filter(name='Barista').exists()

    @property
    def is_customer(self):
        return self.groups.filter(name='Customer').exists()