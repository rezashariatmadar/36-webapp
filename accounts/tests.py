from django.test import TestCase
from .utils import validate_iranian_national_id

class NationalIDValidatorTests(TestCase):
    def test_valid_national_ids(self):
        """Test with known valid national IDs."""
        valid_ids = [
            '0010532415',  # Sample
            '1234567891',  # Hypothetical valid structure check needed
            '0047247736',
        ]
        # Using a few known valid ones or ones constructed to be valid
        # 0047247736: 
        # 0*10 + 0*9 + 4*8 + 7*7 + 2*6 + 4*5 + 7*4 + 7*3 + 3*2 = 32 + 49 + 12 + 20 + 28 + 21 + 6 = 168
        # 168 % 11 = 3
        # remainder 3 >= 2 -> check digit = 11 - 3 = 8. Wait, 0047247736 ends in 6.
        # Let's recompute 0047247736 manually carefully.
        # 0*10=0
        # 0*9=0
        # 4*8=32
        # 7*7=49
        # 2*6=12
        # 4*5=20
        # 7*4=28
        # 7*3=21
        # 3*2=6
        # Sum = 32+49+12+20+28+21+6 = 168. 168 / 11 = 15.27... 11*15=165. Remainder 3.
        # Rule: remainder >= 2 => check=11-remainder => 11-3=8. 
        # So 0047247736 is INVALID based on my manual calc? Or did I mistype?
        # Let's trust the function logic if correct.
        
        # Let's generate a valid one.
        # 123456789 -> sum = 1*10+2*9+3*8+4*7+5*6+6*5+7*4+8*3+9*2
        # = 10 + 18 + 24 + 28 + 30 + 30 + 28 + 24 + 18 = 210
        # 210 % 11 = 1.
        # remainder < 2 => check = remainder = 1.
        # So 1234567891 should be valid.
        self.assertTrue(validate_iranian_national_id('1234567891'))

    def test_invalid_length(self):
        self.assertFalse(validate_iranian_national_id('123'))
        self.assertFalse(validate_iranian_national_id('12345678901'))

    def test_invalid_characters(self):
        self.assertFalse(validate_iranian_national_id('abcdefghij'))
        self.assertFalse(validate_iranian_national_id('123456789a'))

    def test_invalid_checksum(self):
        # 1234567891 is valid (check=1). So 1234567892 should be invalid.
        self.assertFalse(validate_iranian_national_id('1234567892'))

    def test_same_digits(self):
        self.assertFalse(validate_iranian_national_id('1111111111'))
        self.assertFalse(validate_iranian_national_id('0000000000'))

from django.core.exceptions import ValidationError
from .models import CustomUser

class PhoneNumberValidatorTests(TestCase):
    def test_valid_phone_number(self):
        user = CustomUser(phone_number='09123456789')
        user.set_password('testpassword')
        # Should not raise validation error
        user.full_clean()

    def test_invalid_phone_number_length(self):
        user = CustomUser(phone_number='0912345678') # Short
        user.set_password('testpassword')
        with self.assertRaises(ValidationError):
            user.full_clean()
        
        user = CustomUser(phone_number='091234567890') # Long
        user.set_password('testpassword')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number_prefix(self):
        user = CustomUser(phone_number='08123456789') # Wrong prefix
        user.set_password('testpassword')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_invalid_phone_number_chars(self):
        user = CustomUser(phone_number='0912345678a') # Non-digit
        user.set_password('testpassword')
        with self.assertRaises(ValidationError):
            user.full_clean()