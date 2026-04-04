from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auditlog.models import OrderHistory, create_order_history
from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderHistorySerializer,
    OrderListSerializer,
    OrderStatusUpdateSerializer,
)


class BookedDatesAPIView(APIView):
    def get(self, request):
        booked_dates = Order.objects.values_list("booking_date", flat=True)
        return Response(
            {"booked_dates": list(booked_dates)},
            status=status.HTTP_200_OK,
        )


class OrderCreateAPIView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            create_order_history(
                order=order,
                change_type="created",
                comment="Заказ создан через публичное API",
            )

            return Response(
                {
                    "message": "Заказ успешно создан.",
                    "order_id": order.id,
                    "booking_date": order.booking_date,
                    "status": order.status,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.select_related("confirmed_by", "modified_by").all().order_by("booking_date")
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.select_related(
        "confirmed_by",
        "modified_by",
    ).prefetch_related("items__dish__category")
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        old_status = order.status

        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        order.modified_by = request.user

        if order.status == "confirmed" and order.confirmed_by is None:
            order.confirmed_by = request.user
            order.confirmed_at = timezone.now()

        order.save()

        if old_status != order.status:
            create_order_history(
                order=order,
                change_type="status_changed",
                changed_by=request.user,
                field_name="status",
                old_value=old_status,
                new_value=order.status,
                comment="Статус заказа изменён через API сотрудника",
            )

            if order.status == "confirmed":
                create_order_history(
                    order=order,
                    change_type="confirmed",
                    changed_by=request.user,
                    comment="Заказ подтверждён через API сотрудника",
                )

            if order.status == "canceled":
                create_order_history(
                    order=order,
                    change_type="canceled",
                    changed_by=request.user,
                    comment="Заказ отменён через API сотрудника",
                )

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)


class OrderHistoryAPIView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs["pk"]
        return OrderHistory.objects.filter(order_id=order_id).select_related("changed_by").order_by("-created_at")