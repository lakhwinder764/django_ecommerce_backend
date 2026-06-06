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
        return get_user_cart(user)
    return get_session_cart(request)


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
