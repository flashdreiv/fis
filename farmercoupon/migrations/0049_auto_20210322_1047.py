# Generated by Django 3.1.7 on 2021-03-22 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0048_auto_20210322_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='farmer',
            old_name='crop',
            new_name='crops',
        ),
    ]
