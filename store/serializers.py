from rest_framework import serializers
from .models import Category, Product, Cart, CartItem


def _absolute_url(request, path):
    if not path:
        return ''
    if request:
        return request.build_absolute_uri(path)
    return path


def _product_image_url(request, product):
    if product.image:
        return _absolute_url(request, product.image.url)
    return ''


def _product_images(request, product):
    url = _product_image_url(request, product)
    if not url:
        return []
    filename = product.image.name.split('/')[-1] if product.image else 'product.jpg'
    return [{'url': url, 'filename': filename}]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'company',
            'description',
            'price',
            'image',
            'category',
            'colors',
            'featured',
            'stock',
            'stars',
            'reviews',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        return _product_image_url(request, obj)


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'company',
            'description',
            'price',
            'image',
            'category',
            'colors',
            'featured',
            'stock',
            'stars',
            'reviews',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        return _product_images(request, obj)


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'color']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'item_count']

    def get_item_count(self, obj):
        return sum(item.quantity for item in obj.items.all())
