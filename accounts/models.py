import re
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

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


class FreelancerSpecialtyTag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class FreelancerFlair(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    color_token = models.CharField(max_length=32, default="#6d79ff")
    icon_name = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class FreelancerProfile(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING_APPROVAL = "pending_approval", "Pending approval"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"

    class WorkType(models.TextChoices):
        REMOTE = "remote", "Remote"
        ONSITE = "onsite", "Onsite"
        HYBRID = "hybrid", "Hybrid"
        PROJECT_BASED = "project_based", "Project based"

    slug_regex = RegexValidator(
        regex=r"^[a-z0-9-]{3,64}$",
        message="public_slug must contain only lowercase letters, digits, and hyphens (3-64 chars).",
    )

    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name="freelancer_profile")
    public_slug = models.SlugField(max_length=64, unique=True, validators=[slug_regex])
    headline = models.CharField(max_length=180, blank=True)
    introduction = models.TextField(blank=True)
    work_types = models.JSONField(default=list, blank=True)
    city = models.CharField(max_length=120, blank=True)
    province = models.CharField(max_length=120, blank=True)
    is_public = models.BooleanField(default=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DRAFT)
    moderation_note = models.TextField(blank=True)
    contact_cta_text = models.CharField(max_length=80, blank=True, default="Contact me")
    contact_cta_url = models.URLField(blank=True)
    specialties = models.ManyToManyField(FreelancerSpecialtyTag, blank=True, related_name="profiles")
    flairs = models.ManyToManyField(FreelancerFlair, blank=True, related_name="profiles")
    custom_specialties = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def clean(self):
        allowed_work_types = {choice for choice, _ in self.WorkType.choices}
        work_types = self.work_types or []
        if not isinstance(work_types, list):
            raise ValidationError({"work_types": _("work_types must be a list.")})
        if any(work_type not in allowed_work_types for work_type in work_types):
            raise ValidationError({"work_types": _("Invalid work type.")})

        custom_specialties = self.custom_specialties or []
        if not isinstance(custom_specialties, list):
            raise ValidationError({"custom_specialties": _("custom_specialties must be a list.")})
        if len(custom_specialties) > 10:
            raise ValidationError({"custom_specialties": _("At most 10 custom specialties are allowed.")})

        normalized = []
        seen = set()
        for item in custom_specialties:
            if not isinstance(item, str):
                raise ValidationError({"custom_specialties": _("Each custom specialty must be a string.")})
            value = item.strip()
            if not value:
                continue
            if len(value) > 40:
                raise ValidationError({"custom_specialties": _("Each custom specialty must be at most 40 characters.")})
            key = value.casefold()
            if key in seen:
                continue
            seen.add(key)
            normalized.append(value)
        self.custom_specialties = normalized
        self.work_types = list(dict.fromkeys(work_types))

    def __str__(self):
        return f"{self.user.phone_number} ({self.public_slug})"


class FreelancerServiceOffering(models.Model):
    class DeliveryMode(models.TextChoices):
        REMOTE = "remote", "Remote"
        ONSITE = "onsite", "Onsite"
        HYBRID = "hybrid", "Hybrid"

    profile = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    delivery_mode = models.CharField(max_length=16, choices=DeliveryMode.choices, default=DeliveryMode.REMOTE)
    starting_price = models.PositiveIntegerField(default=0)
    response_time_hours = models.PositiveSmallIntegerField(
        default=24,
        validators=[MinValueValidator(1), MaxValueValidator(168)],
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "id"]

    def clean(self):
        if self.starting_price < 0:
            raise ValidationError({"starting_price": _("starting_price must be >= 0.")})

    def __str__(self):
        return self.title
