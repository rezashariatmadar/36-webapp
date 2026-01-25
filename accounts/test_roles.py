from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import Group, AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import CustomUser
from .factories import UserFactory
from .views import VALID_ROLES, change_user_role

class RoleChangeTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_user = UserFactory(phone_number='09120000000')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.admin_user.groups.add(admin_group)
        self.admin_user.refresh_from_db()

        self.target_user = UserFactory(phone_number='09120000001')

    def _get_request(self, user, url):
        request = self.factory.get(url)
        request.user = user
        # Add message support
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request

    def test_valid_roles_constant(self):
        self.assertEqual(VALID_ROLES, ('Admin', 'Barista', 'Customer'))

    def test_change_role_to_barista(self):
        url = reverse('accounts:change_user_role', args=[self.target_user.id, 'Barista'])
        request = self._get_request(self.admin_user, url)

        response = change_user_role(request, self.target_user.id, 'Barista')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:user_list'))

        self.target_user.refresh_from_db()
        self.assertTrue(self.target_user.groups.filter(name='Barista').exists())
        self.assertTrue(self.target_user.is_staff)

    def test_change_role_to_customer(self):
        url = reverse('accounts:change_user_role', args=[self.target_user.id, 'Customer'])
        request = self._get_request(self.admin_user, url)

        response = change_user_role(request, self.target_user.id, 'Customer')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:user_list'))

        self.target_user.refresh_from_db()
        self.assertTrue(self.target_user.groups.filter(name='Customer').exists())
        self.assertFalse(self.target_user.is_staff)

    def test_change_role_invalid(self):
        url = reverse('accounts:change_user_role', args=[self.target_user.id, 'Hacker'])
        request = self._get_request(self.admin_user, url)

        response = change_user_role(request, self.target_user.id, 'Hacker')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:user_list'))

        self.target_user.refresh_from_db()
        self.assertFalse(self.target_user.groups.filter(name='Hacker').exists())
