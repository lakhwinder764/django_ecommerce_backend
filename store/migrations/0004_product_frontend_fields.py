from django.db import migrations, models


def convert_prices_to_paise(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    OrderItem = apps.get_model('store', 'OrderItem')
    Order = apps.get_model('store', 'Order')

    for product in Product.objects.all():
        paise = int(float(product.price) * 100)
        Product.objects.filter(pk=product.pk).update(price=paise)

    for item in OrderItem.objects.all():
        paise = int(float(item.price) * 100)
        OrderItem.objects.filter(pk=item.pk).update(price=paise)

    for order in Order.objects.all():
        paise = int(float(order.total_amount) * 100)
        Order.objects.filter(pk=order.pk).update(total_amount=paise)


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_cart_cartitem'),
    ]

    operations = [
        migrations.RunPython(convert_prices_to_paise, migrations.RunPython.noop),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='stars',
            field=models.FloatField(default=4.5),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='session_key',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                to='auth.user',
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(
                help_text='Price in paise (smallest INR unit)'
            ),
        ),
        migrations.RemoveConstraint(
            model_name='cartitem',
            name='unique_cart_product',
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(
                fields=('cart', 'product', 'color'),
                name='unique_cart_product_color',
            ),
        ),
    ]
