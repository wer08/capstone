# Generated by Django 4.1.3 on 2022-11-07 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_user_calories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='calories',
        ),
    ]