from django.contrib import admin

from .models import MenuCategory, Dish


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "description")
