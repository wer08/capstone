# Generated by Django 4.1.3 on 2022-11-24 12:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0010_remove_daily_daily_calories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='daily_balance',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
    ]