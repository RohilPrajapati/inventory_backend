# Generated by Django 5.0.7 on 2024-09-14 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_stock_updated_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='updated_data',
            new_name='updated_date',
        ),
    ]
