from django.urls import path

from .views import MenuCategoryListAPIView, DishListAPIView

urlpatterns = [
    path("categories/", MenuCategoryListAPIView.as_view(), name="menu-categories"),
    path("dishes/", DishListAPIView.as_view(), name="menu-dishes"),
]