from django.contrib.auth.models import AbstractUser
from django.db import models


class EmployeeUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Администратор"),
        ("manager", "Менеджер"),
        ("staff", "Сотрудник")
    ]

    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    role = models.CharField(
        "Роль",
        max_length=20,
        choices=ROLE_CHOICES,
        default="staff",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновление", auto_now=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["-created_at"]

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name or self.username

