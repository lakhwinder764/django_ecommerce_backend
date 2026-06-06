import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


def _format_inr(paise):
    return f'₹{paise / 100:,.2f}'


def _payment_label(method):
    labels = {
        'card': 'Credit / Debit Card',
        'upi': 'UPI',
        'cod': 'Cash on Delivery',
    }
    return labels.get(method, method)


def build_order_email(order):
    items = list(order.items.select_related('product').all())
    lines = [
        f'Hello {order.full_name},',
        '',
        'Thank you for your order! Here are your order details:',
        '',
        f'Order ID: #{order.id}',
        f'Order date: {timezone.localtime(order.created).strftime("%d %b %Y, %I:%M %p")}',
        f'Status: {order.get_status_display()}',
        f'Payment method: {_payment_label(order.payment_method)}',
        '',
        '--- Items ---',
    ]

    for item in items:
        color = f' ({item.color})' if item.color else ''
        lines.append(
            f'- {item.product.name}{color} x {item.quantity} = '
            f'{_format_inr(item.price * item.quantity)}'
        )

    lines.extend(
        [
            '',
            '--- Summary ---',
            f'Subtotal: {_format_inr(order.subtotal)}',
            f'Shipping: {_format_inr(order.shipping_fee)}',
            f'Total: {_format_inr(order.total_amount)}',
            '',
            '--- Delivery address ---',
            order.full_name,
            order.address,
            f'{order.city}, {order.state} - {order.pincode}',
            f'Phone: {order.phone}',
            f'Email: {order.email}',
            '',
            'You can view this order anytime from the Orders page in your account.',
            '',
            'Thanks for shopping with us!',
            settings.STORE_NAME,
        ]
    )

    subject = f'Order #{order.id} confirmed - {settings.STORE_NAME}'
    message = '\n'.join(lines)
    return subject, message


def send_order_confirmation_email(order):
    if order.user_id and order.user.email:
        recipient = order.user.email
    else:
        recipient = order.email
    if not recipient:
        logger.warning('Order %s has no email; skipping confirmation email.', order.id)
        return False

    subject, message = build_order_email(order)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        logger.info('Order confirmation email sent for order %s to %s', order.id, recipient)
        return True
    except Exception:
        logger.exception(
            'Failed to send order confirmation email for order %s to %s',
            order.id,
            recipient,
        )
        return False
