# Generated by Django 3.1.7 on 2021-03-18 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0021_auto_20210318_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmer',
            name='is_blo',
        ),
    ]
