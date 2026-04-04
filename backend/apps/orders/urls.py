from django.urls import path

from .views import (
    BookedDatesAPIView,
    OrderCreateAPIView,
    OrderDetailAPIView,
    OrderHistoryAPIView,
    OrderListAPIView,
    OrderStatusUpdateAPIView,
)

urlpatterns = [
    path("booked-dates/", BookedDatesAPIView.as_view(), name="booked-dates"),
    path("create/", OrderCreateAPIView.as_view(), name="order-create"),

    path("", OrderListAPIView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("<int:pk>/status/", OrderStatusUpdateAPIView.as_view(), name="order-status-update"),
    path("<int:pk>/history/", OrderHistoryAPIView.as_view(), name="order-history"),
]