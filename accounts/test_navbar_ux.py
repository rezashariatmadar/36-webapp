from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser

class NavbarUXTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='09123456789',
            password='password123',
            full_name='Test User'
        )

    def test_navbar_structure_logged_out(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '۳۶')  # Logo
        # Check for sidebar structure
        self.assertContains(response, 'material-sidebar')
        
        self.assertContains(response, 'منو')
        self.assertContains(response, 'رزرو فضا')
        self.assertContains(response, 'ورود')

    def test_mobile_navigation_present(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        # Check for mobile bottom nav container
        self.assertContains(response, 'md:hidden fixed bottom-6')
        # Check for icons/links implicitly by checking for SVG or links
        self.assertContains(response, 'cafe/menu')
        self.assertContains(response, 'cafe/cart')

    def test_rtl_alignment_classes(self):
        # Check for RTL attribute
        response = self.client.get(reverse('accounts:home'))
        self.assertContains(response, 'dir="rtl"')
