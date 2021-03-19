# Generated by Django 3.1.7 on 2021-03-19 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmercoupon', '0027_auto_20210318_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmer',
            name='user',
        ),
        migrations.AddField(
            model_name='farmer',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='farmer',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]