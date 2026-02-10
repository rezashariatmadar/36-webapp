from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient

from .factories import UserFactory


class StaffUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.admin = UserFactory()
        self.admin.groups.add(admin_group)
        self.user = UserFactory()

    def test_staff_users_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/staff/users/")
        self.assertEqual(response.status_code, 403)

    def test_staff_users_list_and_mutations(self):
        self.client.force_authenticate(user=self.admin)
        list_response = self.client.get("/api/staff/users/")
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(list_response.data["count"], 2)

        status_response = self.client.patch(
            f"/api/staff/users/{self.user.id}/status/",
            {"is_active": False},
            format="json",
        )
        self.assertEqual(status_response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        role_response = self.client.patch(
            f"/api/staff/users/{self.user.id}/role/",
            {"role": "Barista"},
            format="json",
        )
        self.assertEqual(role_response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.groups.filter(name="Barista").exists())
