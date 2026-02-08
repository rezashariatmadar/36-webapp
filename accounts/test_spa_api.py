from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from .factories import UserFactory
from .models import CustomUser


class SessionMeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_me_anonymous(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["authenticated"])
        self.assertIn("csrf_token", response.data)
        self.assertIn("login_url", response.data)

    def test_me_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["authenticated"])
        self.assertEqual(response.data["user"]["id"], self.user.id)
        self.assertIn("roles", response.data["user"])


class SessionAccountAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(phone_number="09127770000")
        self.user.set_password("Pass12345!")
        self.user.save()

    def test_register_logs_user_in_and_assigns_customer_group(self):
        payload = {
            "phone_number": "09129990000",
            "password": "Pass12345!",
            "confirm_password": "Pass12345!",
            "full_name": "New User",
            "national_id": "",
        }
        response = self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["authenticated"])

        created_user = CustomUser.objects.get(phone_number="09129990000")
        customer_group = Group.objects.get(name="Customer")
        self.assertTrue(created_user.groups.filter(id=customer_group.id).exists())

    def test_login_and_logout_cycle(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {"phone_number": "09127770000", "password": "Pass12345!"},
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.data["authenticated"])

        logout_response = self.client.post("/api/auth/logout/", {}, format="json")
        self.assertEqual(logout_response.status_code, 200)
        self.assertFalse(logout_response.data["authenticated"])

    def test_profile_patch_updates_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        patch_response = self.client.patch(
            "/api/auth/profile/",
            {"full_name": "Updated Name", "birth_date": ""},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated Name")

    def test_profile_requires_authentication(self):
        response = self.client.get("/api/auth/profile/")
        self.assertIn(response.status_code, [401, 403])
