from django.conf import settings
from django.db import models


class OrderHistory(models.Model):
    CHANGE_TYPE_CHOICES = [
        ("created", "Создан"),
        ("updated", "Обновлён"),
        ("status_changed", "Статус изменён"),
        ("confirmed", "Подтверждён"),
        ("canceled", "Отменён"),
        ("deleted", "Удалён"),
    ]

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="history_entries",
        verbose_name="Заказ",
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_history_entries",
        verbose_name="Изменил сотрудник",
    )

    change_type = models.CharField(
        "Тип изменения",
        max_length=30,
        choices=CHANGE_TYPE_CHOICES,
    )

    field_name = models.CharField("Поле", max_length=100, blank=True)
    old_value = models.TextField("Старое значение", blank=True)
    new_value = models.TextField("Новое значение", blank=True)
    comment = models.TextField("Комментарий", blank=True)

    created_at = models.DateTimeField("Дата изменения", auto_now_add=True)

    class Meta:
        verbose_name = "История заказа"
        verbose_name_plural = "История заказов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.order_id} - {self.change_type} - {self.created_at}"

    from django.conf import settings
from django.db import models


class OrderHistory(models.Model):
    CHANGE_TYPE_CHOICES = [
        ("created", "Создан"),
        ("updated", "Обновлён"),
        ("status_changed", "Статус изменён"),
        ("confirmed", "Подтверждён"),
        ("canceled", "Отменён"),
        ("deleted", "Удалён"),
    ]

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="history_entries",
        verbose_name="Заказ",
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_history_entries",
        verbose_name="Изменил сотрудник",
    )

    change_type = models.CharField(
        "Тип изменения",
        max_length=30,
        choices=CHANGE_TYPE_CHOICES,
    )

    field_name = models.CharField("Поле", max_length=100, blank=True)
    old_value = models.TextField("Старое значение", blank=True)
    new_value = models.TextField("Новое значение", blank=True)
    comment = models.TextField("Комментарий", blank=True)

    created_at = models.DateTimeField("Дата изменения", auto_now_add=True)

    class Meta:
        verbose_name = "История заказа"
        verbose_name_plural = "История заказов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.order_id} - {self.change_type} - {self.created_at}"


def create_order_history(
    *,
    order,
    change_type,
    changed_by=None,
    field_name="",
    old_value="",
    new_value="",
    comment="",
):
    return OrderHistory.objects.create(
        order=order,
        change_type=change_type,
        changed_by=changed_by,
        field_name=field_name,
        old_value=str(old_value) if old_value is not None else "",
        new_value=str(new_value) if new_value is not None else "",
        comment=comment,    
    )