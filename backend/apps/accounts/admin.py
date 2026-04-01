from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EmployeeUser


@admin.register(EmployeeUser)
class EmployeeUserAdmin(UserAdmin):
    model = EmployeeUser

    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {
            "fields": ("phone", "role", "created_at", "updated_at")
        }),
    )

    readonly_fields = ("created_at", "updated_at")