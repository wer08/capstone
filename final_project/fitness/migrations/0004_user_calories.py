# Generated by Django 4.1.3 on 2022-11-07 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0003_remove_user_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='calories',
            field=models.IntegerField(default=2000),
        ),
    ]
