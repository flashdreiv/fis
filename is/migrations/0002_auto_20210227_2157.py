# Generated by Django 3.1.6 on 2021-02-27 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yfarmer',
            old_name='surname',
            new_name='lastname',
        ),
    ]