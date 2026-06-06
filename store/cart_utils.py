from .models import Cart, CartItem


def _ensure_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_session_cart(request):
    session_key = _ensure_session(request)
    cart, _ = Cart.objects.get_or_create(
        session_key=session_key,
        defaults={'user': None},
    )
    return cart


def get_user_cart(user):
    cart = Cart.objects.filter(user=user).first()
    if cart:
        return cart
    return Cart.objects.create(user=user, session_key=f'user-{user.pk}')


def get_or_create_cart(request):
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        session_cart = get_session_cart(request)
        user_cart = get_user_cart(user)
        return merge_session_cart_into_user_cart(session_cart, user_cart)
    return get_session_cart(request)


def sync_items_to_cart(cart, items_data):
    for entry in items_data:
        product_id = entry.get('product_id')
        quantity = entry.get('quantity', 1)
        color = entry.get('color', '')

        if not product_id or quantity < 1:
            continue

        from .models import Product

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            continue

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            color=color,
            defaults={'quantity': quantity},
        )
        if not created:
            item.quantity = min(item.quantity + quantity, product.stock)
            item.save()
        else:
            item.quantity = min(item.quantity, product.stock)
            item.save()

    return cart


def merge_session_cart_into_user_cart(session_cart, user_cart):
    if session_cart.pk == user_cart.pk:
        return user_cart

    for item in session_cart.items.select_related('product').all():
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            color=item.color,
            defaults={'quantity': item.quantity},
        )
        if not created:
            user_item.quantity = min(
                user_item.quantity + item.quantity,
                item.product.stock,
            )
            user_item.save()

    session_cart.delete()
    return user_cart
