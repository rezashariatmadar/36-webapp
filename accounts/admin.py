from django.contrib import admin
from .models import (
    CustomUser,
    FreelancerFlair,
    FreelancerProfile,
    FreelancerServiceOffering,
    FreelancerSpecialtyTag,
)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'national_id', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'full_name', 'national_id')
    list_filter = ('is_staff', 'is_active', 'groups')
    ordering = ('phone_number',)


class FreelancerServiceOfferingInline(admin.TabularInline):
    model = FreelancerServiceOffering
    extra = 0
    fields = (
        "title",
        "delivery_mode",
        "starting_price",
        "response_time_hours",
        "is_active",
        "sort_order",
    )


@admin.register(FreelancerSpecialtyTag)
class FreelancerSpecialtyTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(FreelancerFlair)
class FreelancerFlairAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_token", "icon_name", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "icon_name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("sort_order", "name")


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ("public_slug", "user", "status", "is_public", "updated_at")
    list_filter = ("status", "is_public")
    search_fields = ("public_slug", "user__phone_number", "user__full_name", "headline", "introduction")
    autocomplete_fields = ("user",)
    filter_horizontal = ("specialties", "flairs")
    readonly_fields = ("created_at", "updated_at")
    inlines = (FreelancerServiceOfferingInline,)


@admin.register(FreelancerServiceOffering)
class FreelancerServiceOfferingAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "delivery_mode", "starting_price", "response_time_hours", "is_active")
    list_filter = ("delivery_mode", "is_active")
    search_fields = ("title", "description", "profile__public_slug", "profile__user__phone_number")
