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

    def test_navbar_structure_logged_in(self):
        self.client.login(phone_number='09123456789', password='password123')
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '۳۶')
        self.assertContains(response, 'Test User')
        # Check for RTL alignment fix class
        self.assertContains(response, 'rtl:left-0')
