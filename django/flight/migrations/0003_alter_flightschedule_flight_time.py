# Generated by Django 5.0.6 on 2024-08-22 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_remove_flightschedule_callsign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightschedule',
            name='flight_time',
            field=models.CharField(max_length=5),
        ),
    ]
