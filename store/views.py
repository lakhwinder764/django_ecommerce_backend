from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product, CartItem
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    CartSerializer,
)
from .cart_utils import (
    get_or_create_cart,
    get_session_cart,
    get_user_cart,
    merge_session_cart_into_user_cart,
)


@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_list(request):
    product_id = request.query_params.get('id')
    featured_only = request.query_params.get('featured')

    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data)

    products = Product.objects.select_related('category').all()
    if featured_only in ('true', '1', 'yes'):
        products = products.filter(featured=True)

    serializer = ProductListSerializer(
        products, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductDetailSerializer(product, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def cart_detail(request):
    cart = get_or_create_cart(request)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def cart_add(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    color = request.data.get('color', '')

    if not product_id:
        return Response(
            {'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return Response(
            {'error': 'quantity must be a positive integer'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if quantity < 1:
        return Response(
            {'error': 'quantity must be at least 1'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        color=color,
        defaults={'quantity': quantity},
    )

    if not created:
        item.quantity += quantity
        if item.quantity > product.stock:
            item.quantity = product.stock
        item.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def cart_update(request):
    product_id = request.data.get('product_id')
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
    color = request.data.get('color', '')

    if quantity is None:
        return Response(
            {'error': 'quantity is required'}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return Response(
            {'error': 'quantity must be an integer'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart = get_or_create_cart(request)

    if item_id:
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    elif product_id:
        item = get_object_or_404(
            CartItem, cart=cart, product_id=product_id, color=color
        )
    else:
        return Response(
            {'error': 'product_id or item_id is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if quantity < 1:
        item.delete()
    else:
        item.quantity = min(quantity, item.product.stock)
        item.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def cart_remove(request):
    product_id = request.data.get('product_id')
    item_id = request.data.get('item_id')
    color = request.data.get('color', '')

    if not product_id and not item_id:
        return Response(
            {'error': 'product_id or item_id is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart = get_or_create_cart(request)

    if item_id:
        item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    else:
        item = get_object_or_404(
            CartItem, cart=cart, product_id=product_id, color=color
        )

    item.delete()
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def cart_clear(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def cart_sync(request):
    user = request.user
    if not user or not user.is_authenticated:
        return Response(
            {'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    session_cart = get_session_cart(request)
    user_cart = get_user_cart(user)
    cart = merge_session_cart_into_user_cart(session_cart, user_cart)
    serializer = CartSerializer(cart)
    return Response(serializer.data)
