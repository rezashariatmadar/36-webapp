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

    def test_spa_primary_routes_and_legacy_redirects(self):
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

        legacy_cafe_redirect = self.client.get("/legacy/cafe/menu/")
        self.assertEqual(legacy_cafe_redirect.status_code, 302)
        self.assertEqual(legacy_cafe_redirect.url, "/app/cafe")

        legacy_cowork_redirect = self.client.get("/legacy/cowork/")
        self.assertEqual(legacy_cowork_redirect.status_code, 302)
        self.assertEqual(legacy_cowork_redirect.url, "/app/cowork")

        legacy_login = self.client.get("/legacy/login/")
        self.assertEqual(legacy_login.status_code, 302)
        self.assertEqual(legacy_login.url, "/app/account")

        legacy_register = self.client.get("/legacy/register/")
        self.assertEqual(legacy_register.status_code, 302)
        self.assertEqual(legacy_register.url, "/app/account")

        legacy_profile = self.client.get("/legacy/profile/")
        self.assertEqual(legacy_profile.status_code, 302)
        self.assertEqual(legacy_profile.url, "/app/account")

        legacy_home = self.client.get("/legacy/")
        self.assertEqual(legacy_home.status_code, 302)
        self.assertEqual(legacy_home.url, "/app")

        legacy_logout = self.client.get("/legacy/logout/")
        self.assertEqual(legacy_logout.status_code, 302)
        self.assertEqual(legacy_logout.url, "/logout/")

        legacy_admin_users = self.client.get("/legacy/admin/users/")
        self.assertEqual(legacy_admin_users.status_code, 302)
        self.assertEqual(legacy_admin_users.url, "/staff/users/")

        legacy_api_users = self.client.get("/legacy/api/users/")
        self.assertEqual(legacy_api_users.status_code, 302)
        self.assertEqual(legacy_api_users.url, "/api/users/")

        user_model = get_user_model()
        staff_user = user_model.objects.create_user(phone_number="09120000003", password="Testpass123!", is_staff=True)
        self.client.force_login(staff_user)
        legacy_dashboard_redirect = self.client.get("/legacy/cafe/dashboard/")
        self.assertEqual(legacy_dashboard_redirect.status_code, 302)
        self.assertEqual(legacy_dashboard_redirect.url, "/app/cafe")

    def test_spa_catchall_excludes_system_routes(self):
        self._reload_urlconf()

        catchall_spa = self.client.get("/random-non-system-path/")
        self.assertEqual(catchall_spa.status_code, 200)
        self.assertContains(catchall_spa, 'id="app-root"')
        self.assertNotContains(catchall_spa, "unpkg.com/htmx.org@2.0.4")
