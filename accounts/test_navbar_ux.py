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
        # Check for split layout container
        self.assertContains(response, 'justify-between')
        # Check for centered nav
        self.assertContains(response, 'flex-1 justify-center')
        
        self.assertContains(response, 'منو')
        self.assertContains(response, 'رزرو فضا')
        self.assertContains(response, 'ورود')

    def test_mobile_navigation_present(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        # Check for mobile bottom nav container
        self.assertContains(response, 'btm-nav md:hidden')
        # Check for bottom nav items
        self.assertContains(response, 'منو')
        self.assertContains(response, 'سبد خرید')
        self.assertContains(response, 'پروفایل')

    def test_rtl_alignment_classes(self):
        # Check for explicit RTL positioning fixes
        response = self.client.get(reverse('accounts:home'))
        self.assertContains(response, 'rtl:left-0')
        self.assertContains(response, 'rtl:right-auto')
