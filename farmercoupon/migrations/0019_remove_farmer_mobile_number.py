# Generated by Django 2.2.7 on 2021-03-18 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0018_farmer_mobile_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmer',
            name='mobile_number',
        ),
    ]