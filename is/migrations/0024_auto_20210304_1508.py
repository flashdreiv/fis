# Generated by Django 2.2.7 on 2021-03-04 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0023_auto_20210303_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleslady',
            name='golden_ticket',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='saleslady',
            name='standard_ticket',
            field=models.IntegerField(default=0),
        ),
    ]
