from django.contrib import admin
from .models import Product
from .models import Category
from .models import Review

from django.contrib import admin
admin.site.site_header = "WEBZon"
admin.site.site_title = "Admin dashboard"
admin.site.index_title = "Welcome!"


# Register your models here.
@admin.register(Review)
class ReviewInLine(admin.TabularInline):
    model = Review.extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInLine]
    list_display = ['name', 'category', 'price', 'is_available', 'created_at', 'colored_status']
    list_filter = ['category', 'is_available', 'created_at']
    autocomplete_fields = ['category']
    search_fields = ['name', 'description']
    list_per_page = 20
    ordering = ['created_at']
    readonly_fields = ['created_at', 'colored_status']
    date_hierarchy = 'created_at'
    list_editable = ['price', 'is_available']

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

    def colored_status(self, obj):
        if obj.is_available:
            return "In stock"
        return "Not available"
    colored_status.short_description = "Status"

    actions = ['make_available', 'make_not_available']

    def make_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, 'Products marked as available.')
    make_available.short_description = 'Mark as available'

    def make_not_available(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, 'Products marked as not available.')
    make_not_available.short_description = 'Mark as not available'