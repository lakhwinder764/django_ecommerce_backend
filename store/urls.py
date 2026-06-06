from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .auth_views import register, me, CustomTokenObtainPairView
from .order_views import checkout, order_list, order_detail

urlpatterns = [
    path('auth/register/', register),
    path('auth/login/', CustomTokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', me),
    path('orders/checkout/', checkout),
    path('orders/', order_list),
    path('orders/<int:pk>/', order_detail),
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('categories/', views.category_list),
    path('cart/', views.cart_detail),
    path('cart/add/', views.cart_add),
    path('cart/update/', views.cart_update),
    path('cart/remove/', views.cart_remove),
    path('cart/clear/', views.cart_clear),
    path('cart/sync/', views.cart_sync),
]
