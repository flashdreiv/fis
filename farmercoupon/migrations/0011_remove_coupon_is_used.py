# Generated by Django 3.1.6 on 2021-03-11 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0010_auto_20210311_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='is_used',
        ),
    ]
