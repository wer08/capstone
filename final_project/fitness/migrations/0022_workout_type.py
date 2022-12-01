# Generated by Django 4.1.3 on 2022-12-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0021_exercise_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='type',
            field=models.CharField(choices=[('Gym', 'Gym'), ('Home', 'Home')], default='Gym', max_length=20),
        ),
    ]