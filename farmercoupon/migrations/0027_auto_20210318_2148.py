# Generated by Django 3.1.7 on 2021-03-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0026_auto_20210318_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='barangay',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='province',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='region',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
