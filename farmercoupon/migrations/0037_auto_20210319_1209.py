# Generated by Django 3.1.7 on 2021-03-19 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0036_auto_20210319_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='barangay',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='province',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='region',
            field=models.CharField(max_length=50, null=True),
        ),
    ]