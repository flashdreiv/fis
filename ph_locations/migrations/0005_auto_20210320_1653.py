# Generated by Django 3.1.7 on 2021-03-20 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ph_locations', '0004_auto_20210320_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangay',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ph_locations.city'),
        ),
        migrations.AlterField(
            model_name='city',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ph_locations.province'),
        ),
    ]