# Generated by Django 4.1.3 on 2022-11-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0006_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='media/pobrane.png', upload_to='media'),
        ),
    ]