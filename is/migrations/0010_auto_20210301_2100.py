# Generated by Django 3.1.6 on 2021-03-01 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0009_products_purchase'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]