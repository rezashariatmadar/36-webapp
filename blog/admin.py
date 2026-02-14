from django.contrib import admin

from .models import BlogPost, BlogTag


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "is_featured", "author")
    list_filter = ("status", "is_featured", "tags")
    search_fields = ("title", "slug", "excerpt", "seo_title", "seo_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    autocomplete_fields = ("author",)

