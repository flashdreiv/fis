# Generated by Django 2.2.7 on 2021-03-18 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0017_remove_farmer_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]