from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    "id",
    "tracking_code",
    "full_name",
    "phone",
    "status",
    "created_at",
    )
    readonly_fields = (
    "full_name",
    "phone",
    "address",
    "postal_code",
    "created_at",
)
    search_fields = (
    "tracking_code",
    "full_name",
    "phone",
)

    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    search_fields = ("full_name", "phone")