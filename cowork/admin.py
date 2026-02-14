from django.contrib import admin
from .models import PricingPlan, Space, Booking

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'daily_rate', 'hourly_rate', 'monthly_rate')

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'capacity', 'pricing_plan', 'is_active')
    list_filter = ('zone', 'is_active')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'space', 'booking_type', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'booking_type', 'space__zone')
    search_fields = ('user__phone_number', 'user__full_name')
    date_hierarchy = 'start_time'
    actions = ("approve_bookings", "mark_cancelled")

    @admin.action(description="Approve selected bookings")
    def approve_bookings(self, request, queryset):
        queryset.update(status=Booking.Status.CONFIRMED)

    @admin.action(description="Mark selected bookings as cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Booking.Status.CANCELLED)
