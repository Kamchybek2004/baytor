# import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.menu.models import Dish

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('canceled', 'Отменён'),
        ('completed', 'Завершён'),
    ]

    booking_date = models.DateField("Дата бронирования", unique=True)

    customer_full_name = models.CharField("ФИО клиента", max_length=255)
    customer_phone = models.CharField("Номер телефон клиента", max_length=20)
    customer_email = models.EmailField("Email клиента")
    comment = models.TextField("Комментарий", blank=True)

    guest_count = models.PositiveIntegerField(
        "Количество гостей",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )

    status = models.CharField(
        "Статус заказа",
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="confirmed_orders",
        verbose_name="Подтвердил",
    )

    confirmed_at = models.DateTimeField("Дата подтверждения", null=True, blank=True)

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="modified_orders",
        verbose_name="Последний редактор",
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["booking_date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(guest_count__gte=1) & models.Q(guest_count__lte=100),
                name="guest_count_between_1_and_100",
            )
        ]

    def __str__(self):
        return f"{self.customer_full_name} - {self.booking_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )

    dish = models.ForeignKey(
        Dish,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Блюдо",
    )

    quantity = models.PositiveIntegerField(
        "Количество",
        validators=[MinValueValidator(1)],
        default=1,
    )

    comment = models.TextField("Комментарий к позиции", blank=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name ="Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        ordering = ["id"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="order_item_quantity_gte_1",
            )
        ]

    def __str__(self):
        return f"Заказ #{self.order_id} - {self.dish.name} X {self.quantity}"