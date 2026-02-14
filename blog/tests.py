from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.factories import UserFactory
from accounts.models import FreelancerProfile
from .models import BlogPost, BlogTag


class BlogPublicAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = UserFactory(full_name="Blog Author")
        self.tag = BlogTag.objects.create(name="Cowork", slug="cowork")
        self.published = BlogPost.objects.create(
            title="Published Post",
            slug="published-post",
            excerpt="published excerpt",
            content_blocks=[{"type": "paragraph", "text": "body"}],
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now() - timedelta(hours=1),
            author=self.author,
            is_featured=True,
        )
        self.published.tags.add(self.tag)
        BlogPost.objects.create(
            title="Draft Post",
            slug="draft-post",
            excerpt="draft excerpt",
            content_blocks=[{"type": "paragraph", "text": "body"}],
            status=BlogPost.Status.DRAFT,
            author=self.author,
        )

    def test_blog_list_returns_only_published_posts(self):
        response = self.client.get("/api/blog/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], "published-post")

    def test_blog_detail_hides_unpublished_posts(self):
        response = self.client.get("/api/blog/posts/draft-post/")
        self.assertEqual(response.status_code, 404)

    def test_blog_tags_payload_contains_post_count(self):
        response = self.client.get("/api/blog/tags/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["tags"][0]["slug"], "cowork")
        self.assertEqual(response.data["tags"][0]["post_count"], 1)


class SeoEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = UserFactory(full_name="Public Freelancer")
        FreelancerProfile.objects.create(
            user=user,
            public_slug="public-freelancer",
            headline="Designer",
            introduction="Bio",
            status=FreelancerProfile.Status.PUBLISHED,
            is_public=True,
        )
        BlogPost.objects.create(
            title="Seo Post",
            slug="seo-post",
            excerpt="seo",
            content_blocks=[{"type": "paragraph", "text": "body"}],
            status=BlogPost.Status.PUBLISHED,
            published_at=timezone.now(),
            author=user,
        )

    def test_sitemap_includes_blog_and_freelancer_links(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("/blog/seo-post/", content)
        self.assertIn("/freelancers/public-freelancer/", content)

    def test_robots_points_to_sitemap(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sitemap:", response.content.decode("utf-8"))

