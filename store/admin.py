from django.contrib import admin
from .models import Category, Product, UserProfile, Order, OrderItem, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'company',
        'price',
        'stock',
        'featured',
        'created',
    )
    list_filter = ('featured', 'category', 'company')
    search_fields = ('name', 'company', 'description')


admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
