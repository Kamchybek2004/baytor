from django.shortcuts import render

from rest_framework import generics

from .models import MenuCategory, Dish
from .serializers import MenuCategorySerializer, DishSerializer


class MenuCategoryListAPIView(generics.ListAPIView):
    queryset = MenuCategory.objects.all().order_by("name")
    serializer_class = MenuCategorySerializer


class DishListAPIView(generics.ListAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        queryset = Dish.objects.filter(is_active=True).select_related("category").order_by("name")

        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset
