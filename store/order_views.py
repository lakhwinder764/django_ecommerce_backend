import logging

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .cart_utils import get_or_create_cart, sync_items_to_cart
from .models import Order, OrderItem, Product
from .order_serializers import CheckoutSerializer, OrderSerializer
from .order_email import send_order_confirmation_email

SHIPPING_FEE = 5000
logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    serializer = CheckoutSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = get_or_create_cart(request)

        items_data = serializer.validated_data.pop('items', None)
        if items_data:
            sync_items_to_cart(cart, items_data)

        cart_items = list(cart.items.select_related('product').all())

        if not cart_items:
            return Response(
                {
                    'error': 'Your cart is empty.',
                    'detail': (
                        'Add items via POST /api/cart/add/ while logged in, '
                        'or include an items array in the checkout request.'
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {
                        'error': (
                            f'Not enough stock for {item.product.name}. '
                            f'Only {item.product.stock} available.'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        shipping_data = serializer.validated_data
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        total_amount = subtotal + SHIPPING_FEE

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                session_key=cart.session_key[:40],
                status='confirmed',
                subtotal=subtotal,
                shipping_fee=SHIPPING_FEE,
                total_amount=total_amount,
                **shipping_data,
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    color=item.color,
                )
                product = Product.objects.select_for_update().get(pk=item.product_id)
                product.stock = max(product.stock - item.quantity, 0)
                product.save(update_fields=['stock'])

            cart.items.all().delete()

        email_sent = send_order_confirmation_email(order)

        return Response(
            {
                'message': 'Order placed successfully.',
                'email_sent': email_sent,
                'order': OrderSerializer(order, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception:
        logger.exception('Checkout failed for user %s', request.user.pk)
        return Response(
            {'error': 'Checkout failed. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related('items__product')
        .order_by('-created')
    )
    serializer = OrderSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        pk=pk,
        user=request.user,
    )
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data)
