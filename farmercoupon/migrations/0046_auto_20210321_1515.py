# Generated by Django 3.1.7 on 2021-03-21 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0045_auto_20210321_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
    ]
