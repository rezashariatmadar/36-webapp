from django.test import TestCase
from django.contrib.auth.models import Group
from cafe.factories import MenuItemFactory
from accounts.factories import UserFactory
from cafe.models import CafeOrder, OrderItem
from django.test.utils import CaptureQueriesContext
from django.db import connection

class PerformanceTests(TestCase):
    def setUp(self):
        # Create Barista group and user
        barista_group, _ = Group.objects.get_or_create(name='Barista')
        self.barista = UserFactory(phone_number='09120000000')
        self.barista.groups.add(barista_group)
        self.client.force_login(self.barista)

        # Create 20 MenuItems
        self.items = MenuItemFactory.create_batch(20, price=1000)

    def test_manual_order_entry_performance(self):
        url = "/cafe/manual-order/"

        # Prepare POST data
        data = {
            'phone_number': '09121111111',
            'notes': 'Performance Test'
        }
        for item in self.items:
            data[f'qty_{item.id}'] = 1

        # Measure queries
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.post(url, data)

        query_count = len(ctx.captured_queries)
        print(f"\nBaseline Query count: {query_count}")

        # Verify correctness
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertEqual(CafeOrder.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 20)

        order = CafeOrder.objects.first()
        self.assertEqual(order.total_price, 20 * 1000)
