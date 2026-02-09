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

    def test_login_validation_and_invalid_credentials(self):
        missing_fields = self.client.post("/api/auth/login/", {"phone_number": ""}, format="json")
        self.assertEqual(missing_fields.status_code, 400)

        invalid_credentials = self.client.post(
            "/api/auth/login/",
            {"phone_number": "09127770000", "password": "wrong-password"},
            format="json",
        )
        self.assertEqual(invalid_credentials.status_code, 400)

    def test_login_with_inactive_user_returns_invalid_credentials_shape(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        response = self.client.post(
            "/api/auth/login/",
            {"phone_number": "09127770000", "password": "Pass12345!"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

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

    def test_profile_get_for_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/auth/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["authenticated"])
        self.assertEqual(response.data["user"]["phone_number"], self.user.phone_number)

    def test_profile_patch_validation_error(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            "/api/auth/profile/",
            {"full_name": "Updated Name", "birth_date": "invalid-date"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.data)

    def test_register_validation_error(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "phone_number": "09123334444",
                "password": "Pass12345!",
                "confirm_password": "different",
                "full_name": "Mismatch User",
                "national_id": "",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_logout_requires_authentication(self):
        response = self.client.post("/api/auth/logout/", {}, format="json")
        self.assertIn(response.status_code, [401, 403])


class StaffManagementAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = UserFactory(phone_number="09127770001")
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.admin.groups.add(admin_group)
        self.target = UserFactory(phone_number="09127770002")

    def test_staff_users_requires_admin(self):
        response = self.client.get("/api/auth/staff/users/")
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.target)
        response = self.client.get("/api/auth/staff/users/")
        self.assertEqual(response.status_code, 403)

    def test_admin_can_list_toggle_and_change_role(self):
        self.client.force_authenticate(user=self.admin)

        listing = self.client.get("/api/auth/staff/users/?page=1&page_size=20")
        self.assertEqual(listing.status_code, 200)
        self.assertIn("results", listing.data)

        status_update = self.client.patch(
            f"/api/auth/staff/users/{self.target.id}/status/",
            {},
            format="json",
        )
        self.assertEqual(status_update.status_code, 200)

        role_update = self.client.patch(
            f"/api/auth/staff/users/{self.target.id}/role/",
            {"role": "Barista"},
            format="json",
        )
        self.assertEqual(role_update.status_code, 200)

        self.target.refresh_from_db()
        self.assertFalse(self.target.is_active)
        self.assertTrue(self.target.groups.filter(name="Barista").exists())
        self.assertTrue(self.target.is_staff)
