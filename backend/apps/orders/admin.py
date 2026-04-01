from django.contrib import admin
from django.utils import timezone

from apps.auditlog.models import create_order_history
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking_date",
        "customer_full_name",
        "customer_phone",
        "customer_email",
        "guest_count",
        "status",
        "confirmed_by",
        "modified_by",
        "created_at",
    )
    list_filter = ("status", "booking_date", "created_at")
    search_fields = (
        "customer_full_name",
        "customer_phone",
        "customer_email",
        "comment",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "confirmed_at",
    )
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_obj = Order.objects.get(pk=obj.pk)
            old_status = old_obj.status
            obj.modified_by = request.user
        else:
            obj.modified_by = request.user

        if obj.status == "confirmed" and obj.confirmed_by is None:
            obj.confirmed_by = request.user
            obj.confirmed_at = timezone.now()

        super().save_model(request, obj, form, change)

        if not change:
            create_order_history(
                order=obj,
                change_type="created",
                changed_by=request.user,
                comment="Заказ создан через админку",
            )
        else:
            if old_status != obj.status:
                create_order_history(
                    order=obj,
                    change_type="status_changed",
                    changed_by=request.user,
                    field_name="status",
                    old_value=old_status,
                    new_value=obj.status,
                    comment="Статус заказа изменён",
                )

                if obj.status == "confirmed":
                    create_order_history(
                        order=obj,
                        change_type="confirmed",
                        changed_by=request.user,
                        comment="Заказ подтверждён",
                    )

                if obj.status == "canceled":
                    create_order_history(
                        order=obj,
                        change_type="canceled",
                        changed_by=request.user,
                        comment="Заказ отменён",
                    )
            else:
                create_order_history(
                    order=obj,
                    change_type="updated",
                    changed_by=request.user,
                    comment="Данные заказа изменены через админку",
                )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in formset.deleted_objects:
            order = obj.order
            dish_name = obj.dish.name
            obj.delete()
            create_order_history(
                order=order,
                change_type="updated",
                changed_by=request.user,
                comment=f"Удалена позиция заказа: {dish_name}",
            )

        for instance in instances:
            is_new = instance.pk is None
            instance.save()

            create_order_history(
                order=instance.order,
                change_type="updated",
                changed_by=request.user,
                comment=(
                    f"Добавлена позиция заказа: {instance.dish.name} x {instance.quantity}"
                    if is_new
                    else f"Изменена позиция заказа: {instance.dish.name} x {instance.quantity}"
                ),
            )

        formset.save_m2m()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "dish", "quantity", "created_at")
    list_filter = ("dish", "created_at")
    search_fields = ("dish__name", "order__customer_full_name")

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)

        create_order_history(
            order=obj.order,
            change_type="updated",
            changed_by=request.user,
            comment=(
                f"Добавлена позиция заказа через отдельную админку: {obj.dish.name} x {obj.quantity}"
                if is_new
                else f"Изменена позиция заказа через отдельную админку: {obj.dish.name} x {obj.quantity}"
            ),
        )

    def delete_model(self, request, obj):
        order = obj.order
        dish_name = obj.dish.name
        super().delete_model(request, obj)

        create_order_history(
            order=order,
            change_type="updated",
            changed_by=request.user,
            comment=f"Удалена позиция заказа через отдельную админку: {dish_name}",
        )