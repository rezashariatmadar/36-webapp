from django.test import TestCase, Client
from django.urls import reverse

class BaseUITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_legacy_home_redirects_to_spa(self):
        response = self.client.get('/legacy/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/app')

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
