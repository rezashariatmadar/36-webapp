from django.test import TestCase, Client
from django.urls import reverse

class BaseUITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_legacy_home_still_renders_template(self):
        response = self.client.get(reverse('accounts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mesh-gradient')
        self.assertContains(response, 'mesh-gradient--liquid')
        self.assertNotContains(response, 'data-rb-island="squares-bg"')

    def test_legacy_cafe_routes_redirect_to_spa(self):
        response = self.client.get('/legacy/cafe/menu/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/cafe')

    def test_auth_portals_redirect_to_spa_account(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app/account')

    def test_root_serves_spa_shell(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')

    def test_spa_shell_mount(self):
        """Verify that the new React SPA shell is served at /app/."""
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')
        self.assertContains(response, 'js/spa-app.js')
