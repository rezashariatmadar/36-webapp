from django.test import TestCase
from django import forms
from .utils import normalize_digits
from .forms_mixins import DigitNormalizationMixin

class NormalizationTests(TestCase):
    def test_utility_function(self):
        self.assertEqual(normalize_digits('۱۲۳۴۵۶۷۸۹۰'), '1234567890')
        self.assertEqual(normalize_digits('٠١٢٣٤٥٦٧٨٩'), '0123456789')
        self.assertEqual(normalize_digits('12345'), '12345')
        self.assertEqual(normalize_digits('تلفن: ۰۹۱۲'), 'تلفن: 0912')

    def test_mixin_explicit_fields(self):
        class TestForm(DigitNormalizationMixin, forms.Form):
            phone = forms.CharField()
            name = forms.CharField()
            normalize_fields = ['phone']

        form = TestForm(data={'phone': '۰۹۱۲', 'name': 'علی ۱۲۳'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone'], '0912')
        self.assertEqual(form.cleaned_data['name'], 'علی ۱۲۳') # Not normalized
