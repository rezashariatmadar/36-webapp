import importlib

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import clear_url_caches

import config.urls as project_urls


class SPARouteCutoverTests(TestCase):
    def _reload_urlconf(self):
        clear_url_caches()
        importlib.reload(project_urls)

    def tearDown(self):
        self._reload_urlconf()

    def test_spa_primary_routes_and_redirects(self):
        self._reload_urlconf()

        root_response = self.client.get("/")
        self.assertEqual(root_response.status_code, 200)
        self.assertContains(root_response, 'id="app-root"')
        self.assertNotContains(root_response, "unpkg.com/htmx.org@2.0.4")

        login_redirect = self.client.get("/login/")
        self.assertEqual(login_redirect.status_code, 302)
        self.assertEqual(login_redirect.url, "/app/account")

        cafe_redirect = self.client.get("/cafe/menu/")
        self.assertEqual(cafe_redirect.status_code, 302)
        self.assertEqual(cafe_redirect.url, "/app/cafe")

        cowork_redirect = self.client.get("/cowork/")
        self.assertEqual(cowork_redirect.status_code, 302)
        self.assertEqual(cowork_redirect.url, "/app/cowork")

        legacy_home = self.client.get("/legacy/")
        self.assertEqual(legacy_home.status_code, 404)

        legacy_cafe = self.client.get("/legacy/cafe/menu/")
        self.assertEqual(legacy_cafe.status_code, 404)

        user_model = get_user_model()
        staff_user = user_model.objects.create_user(phone_number="09120000003", password="Testpass123!", is_staff=True)
        self.client.force_login(staff_user)
        legacy_dashboard = self.client.get("/legacy/cafe/dashboard/")
        self.assertEqual(legacy_dashboard.status_code, 404)

    def test_spa_catchall_excludes_system_routes(self):
        self._reload_urlconf()

        catchall_spa = self.client.get("/random-non-system-path/")
        self.assertEqual(catchall_spa.status_code, 200)
        self.assertContains(catchall_spa, 'id="app-root"')
        self.assertNotContains(catchall_spa, "unpkg.com/htmx.org@2.0.4")
