from django.test import TestCase, Client
from django.urls import reverse

class BaseUITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_liquid_glass_foundations(self):
        """Verify that the base template contains the new Premium Mesh foundations."""
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mesh-gradient')
        self.assertContains(response, 'mesh-gradient--liquid')
        self.assertNotContains(response, 'data-rb-island="squares-bg"')
        self.assertNotContains(response, 'data-rb-island="glass-icons"')
        self.assertNotContains(response, 'data-rb-island="gooey-nav"')

    def test_legacy_pages_mount_react_bits_islands(self):
        response = self.client.get('/legacy/cafe/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-rb-island="squares-bg"')
        self.assertContains(response, 'data-rb-island="glass-icons"')
        self.assertContains(response, 'data-rb-island="gooey-nav"')
        self.assertContains(response, 'reactbits-islands.js')

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

    def test_home_pixel_gallery_mount(self):
        """Verify that the home page includes the pixel gallery mount."""
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-rb-island="pixel-gallery"')

    def test_spa_shell_mount(self):
        """Verify that the new React SPA shell is served at /app/."""
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')
        self.assertContains(response, 'js/spa-app.js')
