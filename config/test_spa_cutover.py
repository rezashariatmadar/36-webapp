import importlib

from django.test import TestCase, override_settings
from django.urls import clear_url_caches, reverse

import config.urls as project_urls


class SPARouteCutoverTests(TestCase):
    def _reload_urlconf(self):
        clear_url_caches()
        importlib.reload(project_urls)

    def tearDown(self):
        self._reload_urlconf()

    @override_settings(SPA_PRIMARY_ROUTES=False)
    def test_default_mode_keeps_legacy_root(self):
        self._reload_urlconf()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-rb-island="pixel-gallery"')
        self.assertNotContains(response, "unpkg.com/htmx.org@2.0.4")
        self.assertNotContains(response, "hx-headers=")

        cafe_redirect = self.client.get("/cafe/menu/")
        self.assertEqual(cafe_redirect.status_code, 302)
        self.assertEqual(cafe_redirect.url, "/legacy/cafe/menu/")

        cowork_redirect = self.client.get("/cowork/")
        self.assertEqual(cowork_redirect.status_code, 302)
        self.assertEqual(cowork_redirect.url, "/legacy/cowork/")

        legacy_cafe = self.client.get("/legacy/cafe/menu/")
        self.assertEqual(legacy_cafe.status_code, 200)
        self.assertContains(legacy_cafe, "unpkg.com/htmx.org@2.0.4")
        self.assertContains(legacy_cafe, "hx-headers=")

        self.assertEqual(reverse("cafe:menu"), "/legacy/cafe/menu/")
        self.assertEqual(reverse("cowork:space_list"), "/legacy/cowork/")

    @override_settings(SPA_PRIMARY_ROUTES=True)
    def test_spa_primary_mode_routes_and_legacy_fallback(self):
        self._reload_urlconf()

        root_response = self.client.get("/")
        self.assertEqual(root_response.status_code, 200)
        self.assertContains(root_response, 'id="app-root"')

        login_redirect = self.client.get("/login/")
        self.assertEqual(login_redirect.status_code, 302)
        self.assertEqual(login_redirect.url, "/app/account")

        cafe_redirect = self.client.get("/cafe/menu/")
        self.assertEqual(cafe_redirect.status_code, 302)
        self.assertEqual(cafe_redirect.url, "/app/cafe")

        cowork_redirect = self.client.get("/cowork/")
        self.assertEqual(cowork_redirect.status_code, 302)
        self.assertEqual(cowork_redirect.url, "/app/cowork")

        legacy_login = self.client.get("/legacy/login/")
        self.assertEqual(legacy_login.status_code, 200)

        legacy_cafe = self.client.get("/legacy/cafe/menu/")
        self.assertEqual(legacy_cafe.status_code, 200)
        self.assertContains(legacy_cafe, "unpkg.com/htmx.org@2.0.4")

        catchall_spa = self.client.get("/random-non-system-path/")
        self.assertEqual(catchall_spa.status_code, 200)
        self.assertContains(catchall_spa, 'id="app-root"')
        self.assertNotContains(catchall_spa, "unpkg.com/htmx.org@2.0.4")
