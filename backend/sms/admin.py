
from django.contrib import admin
from .models import Purchase, IssuedItem, Items, Faculty, Department


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = (
        "name", "totalPurchased", "ItemsIssued",
        "QuantityInInventory", "is_active"
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)
    actions = ["deactivate_items", "activate_items"]

    @admin.action(description="Deactivate selected items")
    def deactivate_items(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Activate selected items")
    def activate_items(self, request, queryset):
        queryset.update(is_active=True)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty_id", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "faculty_id")
    list_editable = ("is_active",)
    actions = ["deactivate_faculty", "activate_faculty"]

    @admin.action(description="Deactivate selected faculty")
    def deactivate_faculty(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Activate selected faculty")
    def activate_faculty(self, request, queryset):
        queryset.update(is_active=True)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department",)
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IssuedItem)
class IssuedItemAdmin(admin.ModelAdmin):
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False
