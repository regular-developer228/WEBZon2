from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name', 'description']
    list_per_page = 20
    ordering = ['created_at']
    readonly_fields = ['created_at']
    date_hierarchy = "created_at"

    fieldsets = (
        ("Main Info", {
            "fields": ('name', 'description')
        }),
        ("Secondary Info", {
            "fields": ('price', 'is_available')
        }),
        ("Others", {
            "fields": ('created_at',),
            "classes": ('collapse',)
        })
    )
