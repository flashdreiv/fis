# Generated by Django 3.1.6 on 2021-03-01 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0010_auto_20210301_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='item_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='is.purchase'),
        ),
    ]