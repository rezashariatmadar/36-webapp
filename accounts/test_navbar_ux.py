from django.test import TestCase
from django.urls import reverse


class NavbarUXTests(TestCase):
    def test_legacy_home_redirects_to_spa(self):
        response = self.client.get(reverse("accounts:home"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app")

    def test_spa_shell_mount_present(self):
        response = self.client.get("/app/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')
        self.assertContains(response, "js/spa-app.js")

    def test_spa_shell_rtl_attribute(self):
        response = self.client.get("/app/")
        self.assertContains(response, 'dir="rtl"')
