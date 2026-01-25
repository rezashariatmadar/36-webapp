from django.test import TestCase, Client
from django.urls import reverse

class BaseUITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_liquid_glass_foundations(self):
        """Verify that the base template contains the new Premium Mesh foundations."""
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for the HTML structure
        self.assertContains(response, '<div class="mesh-gradient"></div>')

    def test_auth_portals(self):
        """Verify that Login and Register pages use the premium material layout."""
        # Test Login
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'material-glass')
        self.assertContains(response, 'btn-apple-primary')
        
        # Test Register
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'material-glass')
        self.assertContains(response, 'btn-apple-primary')
