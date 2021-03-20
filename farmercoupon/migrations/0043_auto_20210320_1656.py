# Generated by Django 3.1.7 on 2021-03-20 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ph_locations', '0005_auto_20210320_1653'),
        ('farmercoupon', '0042_auto_20210320_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer',
            name='barangay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ph_locations.barangay'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ph_locations.city'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ph_locations.province'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ph_locations.region'),
        ),
    ]