# Generated by Django 3.1.6 on 2021-03-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0012_auto_20210301_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='item_category',
            field=models.CharField(choices=[('Aljay Chemicals', 'Aljay Chemicals'), ('Allied Chemicals', 'Allied Chemicals'), ('Fertilizer', 'Fertilizer')], max_length=50, null=True),
        ),
    ]
