# Generated by Django 4.1.7 on 2023-06-06 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0002_remove_cartitem_cart_remove_cartitem_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Cart',
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=250)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Order Total')),
                ('emailAddress', models.EmailField(blank=True, max_length=250, verbose_name='Email Address')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('billingName', models.CharField(blank=True, max_length=250)),
                ('billingAddress1', models.CharField(blank=True, max_length=250)),
                ('billingCity', models.CharField(blank=True, max_length=250)),
                ('billingPostcode', models.CharField(blank=True, max_length=250)),
                ('billingCountry', models.CharField(blank=True, max_length=250)),
                ('shippingName', models.CharField(blank=True, max_length=250)),
                ('shippingAddress1', models.CharField(blank=True, max_length=250)),
                ('shippingCity', models.CharField(blank=True, max_length=250)),
                ('shippingPostcode', models.CharField(blank=True, max_length=250)),
                ('shippingCountry', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'db_table': 'Order',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='profile/avatar.jpg', upload_to='profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=250)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Price')),
                ('choosen_informations', models.TextField(help_text='string of json of extra information of item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.order')),
            ],
            options={
                'db_table': 'OrderItem',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('choosen_informations', models.TextField(help_text='string of json of extra information of item')),
                ('active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'db_table': 'CartItem',
            },
        ),
    ]
