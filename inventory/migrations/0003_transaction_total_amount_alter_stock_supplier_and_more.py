# Generated by Django 5.0.7 on 2024-09-13 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_stock_product_alter_stock_supplier_and_more'),
        ('products', '0004_alter_product_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='stock',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stocks_supplier', to='products.supplier'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_no',
            field=models.CharField(max_length=100, null=True),
        ),
    ]