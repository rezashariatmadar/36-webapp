from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'national_id', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'full_name', 'national_id')
    list_filter = ('is_staff', 'is_active', 'groups')
    ordering = ('phone_number',)
