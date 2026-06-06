from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )
    company = models.CharField(max_length=100, default='Unknown')
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(
        help_text='Price in paise (smallest INR unit)'
    )
    image = models.ImageField(upload_to='products/', blank=True)
    stock = models.PositiveIntegerField(default=10)
    featured = models.BooleanField(default=False)
    stars = models.FloatField(default=4.5)
    reviews = models.PositiveIntegerField(default=0)
    colors = models.JSONField(default=list, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    subtotal = models.PositiveIntegerField(default=0)
    shipping_fee = models.PositiveIntegerField(default=5000)
    total_amount = models.PositiveIntegerField(default=0)
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    payment_method = models.CharField(max_length=20, default='card')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    color = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, blank=True, default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product', 'color'],
                name='unique_cart_product_color',
            ),
        ]

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
