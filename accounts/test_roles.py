from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from .factories import UserFactory
from .api_views import VALID_ROLES

class RoleChangeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = UserFactory(phone_number='09120000000')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.admin_user.groups.add(admin_group)
        self.admin_user.refresh_from_db()

        self.target_user = UserFactory(phone_number='09120000001')
        self.client.force_authenticate(user=self.admin_user)

    def test_valid_roles_constant(self):
        self.assertEqual(VALID_ROLES, ('Admin', 'Barista', 'Customer'))

    def test_change_role_to_barista(self):
        response = self.client.patch(
            f"/api/auth/staff/users/{self.target_user.id}/role/",
            {"role": "Barista"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.target_user.refresh_from_db()
        self.assertTrue(self.target_user.groups.filter(name='Barista').exists())
        self.assertTrue(self.target_user.is_staff)

    def test_change_role_to_customer(self):
        response = self.client.patch(
            f"/api/auth/staff/users/{self.target_user.id}/role/",
            {"role": "Customer"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.target_user.refresh_from_db()
        self.assertTrue(self.target_user.groups.filter(name='Customer').exists())
        self.assertFalse(self.target_user.is_staff)

    def test_change_role_invalid(self):
        response = self.client.patch(
            f"/api/auth/staff/users/{self.target_user.id}/role/",
            {"role": "Hacker"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        self.target_user.refresh_from_db()
        self.assertFalse(self.target_user.groups.filter(name='Hacker').exists())

    def test_toggle_status(self):
        response = self.client.patch(
            f"/api/auth/staff/users/{self.target_user.id}/status/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.target_user.refresh_from_db()
        self.assertFalse(self.target_user.is_active)

    def test_toggle_status_rejects_self(self):
        response = self.client.patch(
            f"/api/auth/staff/users/{self.admin_user.id}/status/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
