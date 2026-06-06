# Generated manually for checkout fields

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_frontend_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='stripe_session_id',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default='card', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='order',
            name='pincode',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_fee',
            field=models.PositiveIntegerField(default=5000),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('confirmed', 'Confirmed'),
                    ('processing', 'Processing'),
                    ('shipped', 'Shipped'),
                    ('delivered', 'Delivered'),
                    ('cancelled', 'Cancelled'),
                ],
                default='confirmed',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='color',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created']},
        ),
    ]
