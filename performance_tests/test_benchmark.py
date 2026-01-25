from django.test import TestCase
from cowork.models import Space
from cowork.factories import SpaceFactory
from django.db import connection
from django.test.utils import CaptureQueriesContext

class RefreshStatusBenchmark(TestCase):
    def setUp(self):
        self.space = SpaceFactory(status=Space.Status.AVAILABLE)

    def test_refresh_status_queries_no_change(self):
        """
        Test that refresh_status triggers a database write even if status doesn't change.
        Current behavior: 1 SELECT (exists) + 1 UPDATE (save) = 2 queries.
        Target behavior: 1 SELECT (exists) + 0 UPDATE = 1 query.
        """
        # Ensure initial state
        self.assertEqual(self.space.status, Space.Status.AVAILABLE)

        # We expect 2 queries:
        # 1. SELECT to check for active bookings (.exists())
        # 2. UPDATE to save the space (even though status is same)
        with CaptureQueriesContext(connection) as ctx:
            self.space.refresh_status()

        print(f"\nQueries executed: {len(ctx.captured_queries)}")
        for i, query in enumerate(ctx.captured_queries):
            print(f"{i+1}. {query['sql']}")

        # Assert optimized behavior
        # We expect 1 query:
        # 1. SELECT to check for active bookings (.exists())
        # 0. UPDATE (saved avoided)
        self.assertEqual(len(ctx.captured_queries), 1, "Expected exactly 1 query (Select only)")

        # Verify it DOES NOT include an UPDATE
        update_queries = [q for q in ctx.captured_queries if 'UPDATE' in q['sql']]
        self.assertEqual(len(update_queries), 0, "Expected NO UPDATE query")
