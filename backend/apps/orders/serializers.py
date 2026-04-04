from rest_framework import serializers

from apps.auditlog.models import OrderHistory
from apps.menu.models import Dish
from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_dish_id(self, value):
        if not Dish.objects.filter(id=value).exists():
            raise serializers.ValidationError("Блюдо не найдено.")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "booking_date",
            "customer_full_name",
            "customer_phone",
            "customer_email",
            "comment",
            "guest_count",
            "items",
        ]

    def validate_booking_date(self, value):
        if Order.objects.filter(booking_date=value).exists():
            raise serializers.ValidationError("На эту дату заказ уже существует.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            dish = Dish.objects.get(id=item_data["dish_id"])
            OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=item_data["quantity"],
                comment=item_data.get("comment", ""),
            )

        return order


class OrderItemReadSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)
    category_name = serializers.CharField(source="dish.category.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "dish",
            "dish_name",
            "category_name",
            "quantity",
            "comment",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    confirmed_by_username = serializers.CharField(source="confirmed_by.username", read_only=True)
    modified_by_username = serializers.CharField(source="modified_by.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "booking_date",
            "customer_full_name",
            "customer_phone",
            "customer_email",
            "guest_count",
            "status",
            "confirmed_by",
            "confirmed_by_username",
            "modified_by",
            "modified_by_username",
            "created_at",
            "updated_at",
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)
    confirmed_by_username = serializers.CharField(source="confirmed_by.username", read_only=True)
    modified_by_username = serializers.CharField(source="modified_by.username", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "booking_date",
            "customer_full_name",
            "customer_phone",
            "customer_email",
            "comment",
            "guest_count",
            "status",
            "confirmed_by",
            "confirmed_by_username",
            "confirmed_at",
            "modified_by",
            "modified_by_username",
            "created_at",
            "updated_at",
            "items",
        ]


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError("Недопустимый статус заказа.")
        return value


class OrderHistorySerializer(serializers.ModelSerializer):
    changed_by_username = serializers.CharField(source="changed_by.username", read_only=True)

    class Meta:
        model = OrderHistory
        fields = [
            "id",
            "change_type",
            "field_name",
            "old_value",
            "new_value",
            "comment",
            "changed_by",
            "changed_by_username",
            "created_at",
        ]