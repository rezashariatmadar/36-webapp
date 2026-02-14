from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class BlogTag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    excerpt = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="blog/posts/hero/", blank=True, null=True)
    hero_image_alt = models.CharField(max_length=200, blank=True)
    content_blocks = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
    )
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.CharField(max_length=320, blank=True)
    canonical_url = models.URLField(blank=True)
    og_image = models.ImageField(upload_to="blog/posts/og/", blank=True, null=True)
    geo_city = models.CharField(max_length=120, blank=True)
    geo_region = models.CharField(max_length=120, blank=True)
    geo_country = models.CharField(max_length=2, default="IR")
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(BlogTag, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def clean(self):
        blocks = self.content_blocks or []
        if not isinstance(blocks, list):
            raise ValidationError({"content_blocks": "content_blocks must be a list."})

        allowed_types = {"paragraph", "heading", "image", "quote", "list"}
        for index, block in enumerate(blocks):
            if not isinstance(block, dict):
                raise ValidationError({"content_blocks": f"Block {index} must be an object."})

            block_type = block.get("type")
            if block_type not in allowed_types:
                raise ValidationError({"content_blocks": f"Block {index} has unsupported type."})

            if block_type in {"paragraph", "heading", "quote"}:
                if not isinstance(block.get("text"), str) or not block.get("text", "").strip():
                    raise ValidationError({"content_blocks": f"Block {index} requires non-empty text."})

            if block_type == "image":
                if not isinstance(block.get("url"), str) or not block.get("url", "").strip():
                    raise ValidationError({"content_blocks": f"Image block {index} requires url."})

            if block_type == "list":
                items = block.get("items")
                if not isinstance(items, list) or not items:
                    raise ValidationError({"content_blocks": f"List block {index} requires items."})
                if any(not isinstance(item, str) or not item.strip() for item in items):
                    raise ValidationError({"content_blocks": f"List block {index} items must be non-empty strings."})

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

    def __str__(self):
        return self.title

