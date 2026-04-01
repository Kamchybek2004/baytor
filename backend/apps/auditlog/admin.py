from django.contrib import admin

from .models import OrderHistory


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "change_type",
        "changed_by",
        "field_name",
        "created_at",
    )
    list_filter = ("change_type", "created_at")
    search_fields = (
        "order__customer_full_name",
        "field_name",
        "old_value",
        "new_value",
        "comment",
    )
    readonly_fields = ("created_at",)