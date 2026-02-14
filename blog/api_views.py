from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BlogPost, BlogTag


def _parse_bool(value: str | None):
    if value is None:
        return None
    lowered = value.lower().strip()
    if lowered in {"1", "true", "yes"}:
        return True
    if lowered in {"0", "false", "no"}:
        return False
    return None


def _image_url(request, image_field):
    if not image_field:
        return None
    return request.build_absolute_uri(image_field.url)


def _serialize_tag(tag: BlogTag):
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug,
    }


def _serialize_post_card(request, post: BlogPost):
    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "excerpt": post.excerpt,
        "hero_image_url": _image_url(request, post.hero_image),
        "hero_image_alt": post.hero_image_alt,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "is_featured": post.is_featured,
        "seo_title": post.seo_title,
        "seo_description": post.seo_description,
        "geo_city": post.geo_city,
        "geo_region": post.geo_region,
        "geo_country": post.geo_country,
        "tags": [_serialize_tag(tag) for tag in post.tags.all()],
    }


def _published_posts_qs():
    return (
        BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED).filter(
            Q(published_at__isnull=True) | Q(published_at__lte=timezone.now())
        )
        .select_related("author")
        .prefetch_related("tags")
        .distinct()
    )


class BlogPostsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = (request.query_params.get("q") or "").strip()
        tag = (request.query_params.get("tag") or "").strip()
        city = (request.query_params.get("city") or "").strip()
        featured = _parse_bool(request.query_params.get("featured"))
        page = max(int(request.query_params.get("page", 1)), 1)
        page_size = min(max(int(request.query_params.get("page_size", 10)), 1), 100)

        posts = _published_posts_qs()
        if query:
            posts = posts.filter(
                Q(title__icontains=query)
                | Q(excerpt__icontains=query)
                | Q(seo_title__icontains=query)
                | Q(seo_description__icontains=query)
            )
        if tag:
            posts = posts.filter(tags__slug=tag)
        if city:
            posts = posts.filter(geo_city__icontains=city)
        if featured is not None:
            posts = posts.filter(is_featured=featured)

        total = posts.count()
        offset = (page - 1) * page_size
        chunk = posts[offset : offset + page_size]
        return Response(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": [_serialize_post_card(request, post) for post in chunk],
            }
        )


class BlogPostDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        post = get_object_or_404(_published_posts_qs(), slug=slug)
        related = (
            _published_posts_qs()
            .filter(tags__in=post.tags.all())
            .exclude(id=post.id)
            .order_by("-published_at", "-id")
            .distinct()[:3]
        )
        return Response(
            {
                "post": {
                    **_serialize_post_card(request, post),
                    "content_blocks": post.content_blocks,
                    "canonical_url": post.canonical_url,
                    "og_image_url": _image_url(request, post.og_image),
                    "author_name": post.author.full_name if post.author else "",
                },
                "related": [_serialize_post_card(request, item) for item in related],
            }
        )


class BlogTagsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tags = (
            BlogTag.objects.filter(is_active=True)
            .annotate(
                post_count=Count(
                    "posts",
                    filter=Q(
                        posts__status=BlogPost.Status.PUBLISHED,
                        posts__published_at__lte=timezone.now(),
                    ),
                    distinct=True,
                )
            )
            .order_by("sort_order", "name")
        )
        return Response(
            {
                "tags": [
                    {
                        "id": tag.id,
                        "name": tag.name,
                        "slug": tag.slug,
                        "post_count": tag.post_count,
                    }
                    for tag in tags
                ]
            }
        )
