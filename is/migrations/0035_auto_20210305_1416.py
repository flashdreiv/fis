# Generated by Django 2.2.7 on 2021-03-05 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('is', '0034_auto_20210305_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='code',
            field=models.CharField(default=0, max_length=15, unique=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='farmer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='is.Farmer'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='is_golden_ticket',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coupon',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coupon',
            name='saleslady',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='is.SalesLady'),
        ),
        migrations.AlterField(
            model_name='farmer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]