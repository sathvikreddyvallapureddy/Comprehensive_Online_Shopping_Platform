# Generated by Django 4.0.1 on 2022-05-07 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=150)),
                ('lname', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
                ('pincode', models.CharField(max_length=150)),
                ('total_price', models.CharField(max_length=150)),
                ('payment_mode', models.CharField(max_length=150)),
                ('payment_id', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Completed', 'Completed')], default='Pending', max_length=150)),
                ('message', models.TextField(null=True)),
                ('tracking_no', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
    ]
