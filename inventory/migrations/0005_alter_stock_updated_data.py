# Generated by Django 5.0.7 on 2024-09-14 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_stock_updated_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='updated_data',
            field=models.DateTimeField(null=True),
        ),
    ]
