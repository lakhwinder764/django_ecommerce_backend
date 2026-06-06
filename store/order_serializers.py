from rest_framework import serializers

from .models import Order, OrderItem, Product
from .serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'color']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'subtotal',
            'shipping_fee',
            'total_amount',
            'full_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'pincode',
            'payment_method',
            'created',
            'items',
            'item_count',
        ]

    def get_item_count(self, obj):
        return sum(item.quantity for item in obj.items.all())


class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    color = serializers.CharField(required=False, allow_blank=True, default='')


class CheckoutSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=10)
    payment_method = serializers.ChoiceField(
        choices=['card', 'upi', 'cod'],
        default='card',
    )
    items = CheckoutItemSerializer(many=True, required=False)

    def validate_phone(self, value):
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 10:
            raise serializers.ValidationError('Enter a valid phone number.')
        return value

    def validate_pincode(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('Enter a valid 6-digit pincode.')
        return value
