# Generated by Django 3.1.6 on 2021-03-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0021_auto_20210303_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]