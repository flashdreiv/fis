# Generated by Django 3.1.7 on 2021-03-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0020_farmer_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleslady',
            name='branch_name',
            field=models.CharField(max_length=30),
        ),
    ]
