# Generated by Django 5.0.7 on 2024-09-28 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_stock_minimum_stock_level'),
        ('products', '0005_alter_product_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='products.supplier'),
            preserve_default=False,
        ),
    ]