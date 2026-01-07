from django.contrib import admin
from .models import MenuCategory, MenuItem, CafeOrder, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(CafeOrder)
class CafeOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__phone_number', 'notes')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')