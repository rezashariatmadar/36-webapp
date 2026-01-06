from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group, AnonymousUser
from django.http import HttpResponse
from django.urls import reverse
from .factories import UserFactory
from .utils import admin_required, barista_required, customer_required

@admin_required
def dummy_admin_view(request):
    return HttpResponse("Admin Access")

@barista_required
def dummy_barista_view(request):
    return HttpResponse("Barista Access")

@customer_required
def dummy_customer_view(request):
    return HttpResponse("Customer Access")

class RBACDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.barista_group, _ = Group.objects.get_or_create(name='Barista')
        self.customer_group, _ = Group.objects.get_or_create(name='Customer')

    def test_admin_required_as_admin(self):
        user = UserFactory()
        user.groups.add(self.admin_group)
        request = self.factory.get('/dummy-admin/')
        request.user = user
        response = dummy_admin_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Admin Access")

    def test_admin_required_as_barista(self):
        user = UserFactory()
        user.groups.add(self.barista_group)
        request = self.factory.get('/dummy-admin/')
        request.user = user
        with self.assertRaises(Exception): # PermissionDenied
             dummy_admin_view(request)

    def test_admin_required_anonymous(self):
        request = self.factory.get('/dummy-admin/')
        request.user = AnonymousUser()
        response = dummy_admin_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_barista_required_as_barista(self):
        user = UserFactory()
        user.groups.add(self.barista_group)
        request = self.factory.get('/dummy-barista/')
        request.user = user
        response = dummy_barista_view(request)
        self.assertEqual(response.status_code, 200)

    def test_barista_required_as_admin(self):
        user = UserFactory()
        user.groups.add(self.admin_group)
        request = self.factory.get('/dummy-barista/')
        request.user = user
        response = dummy_barista_view(request)
        self.assertEqual(response.status_code, 200)

    def test_barista_required_as_customer(self):
        user = UserFactory()
        user.groups.add(self.customer_group)
        request = self.factory.get('/dummy-barista/')
        request.user = user
        with self.assertRaises(Exception):
            dummy_barista_view(request)

    def test_customer_required_as_customer(self):
        user = UserFactory()
        user.groups.add(self.customer_group)
        request = self.factory.get('/dummy-customer/')
        request.user = user
        response = dummy_customer_view(request)
        self.assertEqual(response.status_code, 200)
