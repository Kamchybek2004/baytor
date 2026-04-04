from rest_framework import serializers

from .models import MenuCategory, Dish


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ["id", "name", "description"]


class DishSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(source="category.id", read_only=True)

    class Meta:
        model = Dish
        fields = ["id", "name", "description", "is_active", "category", "category_id"]