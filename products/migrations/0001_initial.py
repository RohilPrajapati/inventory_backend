# Generated by Django 5.0.7 on 2024-07-29 13:48

import datetime
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('address', models.CharField(max_length=155, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=255, null=True)),
                ('postal_code', models.ImageField(null=True, upload_to='')),
                ('country', models.CharField(max_length=170, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250)),
                ('description', models.TextField(null=True)),
                ('sku', models.CharField(max_length=50, null=True, unique=True)),
                ('upc', models.CharField(max_length=50, null=True, unique=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_date', models.DateTimeField(default=datetime.datetime.now)),
                ('weight', models.IntegerField(null=True)),
                ('dimensions', models.CharField(null=True)),
                ('color', models.CharField(blank=True, null=True)),
                ('size', models.CharField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='products.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
