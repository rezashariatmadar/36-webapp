from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser, validate_iranian_national_id
from .factories import UserFactory

class NationalIDValidatorTests(TestCase):
    def test_valid_national_ids(self):
        """Test with known valid national IDs."""
        # 1234567891 is valid:
        # 1*10 + 2*9 + 3*8 + 4*7 + 5*6 + 6*5 + 7*4 + 8*3 + 9*2 = 210
        # 210 % 11 = 1. Remainder < 2, so check digit must be 1.
        self.assertTrue(validate_iranian_national_id('1234567891'))
        
        # 0010532415
        # 0*10 + 0*9 + 1*8 + 0*7 + 5*6 + 3*5 + 2*4 + 4*3 + 1*2 = 8 + 30 + 15 + 8 + 12 + 2 = 75
        # 75 % 11 = 9. Remainder >= 2, so check digit must be 11 - 9 = 2.
        # Wait, 0010532415 ends in 5.
        # 0*10=0, 0*9=0, 1*8=8, 0*7=0, 5*6=30, 3*5=15, 2*4=8, 4*3=12, 1*2=2. Sum=75. 75/11=6.8... 11*6=66. Remainder 9.
        # 11-9=2. So 0010532415 is invalid.
        # Let's check a real one: 0047247736 (I calculated this before, remainder 3, check should be 11-3=8).
        # Let's try 0010532412.
        self.assertTrue(validate_iranian_national_id('1234567891'))
        self.assertTrue(validate_iranian_national_id('0010532412'))

    def test_invalid_length(self):
        self.assertFalse(validate_iranian_national_id('123'))
        self.assertFalse(validate_iranian_national_id('12345678901'))

    def test_invalid_characters(self):
        self.assertFalse(validate_iranian_national_id('abcdefghij'))
        self.assertFalse(validate_iranian_national_id('123456789a'))

    def test_invalid_checksum(self):
        self.assertFalse(validate_iranian_national_id('1234567892'))

    def test_same_digits(self):
        self.assertFalse(validate_iranian_national_id('1111111111'))
        self.assertFalse(validate_iranian_national_id('0000000000'))

class PhoneNumberValidatorTests(TestCase):
    def test_valid_phone_number(self):
        user = UserFactory.build(phone_number='09123456789')
        # Should not raise validation error
        user.full_clean()

    def test_invalid_phone_number_length(self):
        user = UserFactory.build(phone_number='0912345678') # Short
        with self.assertRaises(ValidationError):
            user.full_clean()
        
        user = UserFactory.build(phone_number='091234567890') # Long
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number_prefix(self):
        user = UserFactory.build(phone_number='08123456789') # Wrong prefix
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number_chars(self):
        user = UserFactory.build(phone_number='0912345678a') # Non-digit
        with self.assertRaises(ValidationError):
            user.full_clean()

class CustomUserModelTests(TestCase):
    def test_create_user(self):
        user = UserFactory()
        self.assertEqual(user.groups.count(), 0)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_user_is_admin_property(self):
        user = UserFactory()
        self.assertFalse(user.is_admin)
        from django.contrib.auth.models import Group
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        user.groups.add(admin_group)
        self.assertTrue(user.is_admin)

    def test_user_is_barista_property(self):
        user = UserFactory()
        self.assertFalse(user.is_barista)
        from django.contrib.auth.models import Group
        barista_group, _ = Group.objects.get_or_create(name='Barista')
        user.groups.add(barista_group)
        self.assertTrue(user.is_barista)

    def test_user_is_customer_property(self):
        user = UserFactory()
        self.assertFalse(user.is_customer)
        from django.contrib.auth.models import Group
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        user.groups.add(customer_group)
        self.assertTrue(user.is_customer)