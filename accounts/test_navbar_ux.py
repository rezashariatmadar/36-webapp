from django.test import TestCase
from django.urls import reverse


class NavbarUXTests(TestCase):
    def test_root_serves_spa_shell(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')

    def test_spa_shell_mount_present(self):
        response = self.client.get("/app/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="app-root"')
        self.assertContains(response, "js/spa-app.js")

    def test_spa_shell_rtl_attribute(self):
        response = self.client.get("/app/")
        self.assertContains(response, 'dir="rtl"')
