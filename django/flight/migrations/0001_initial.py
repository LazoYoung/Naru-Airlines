# Generated by Django 5.0.6 on 2024-07-20 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passenger', '0001_initial'),
        ('pilot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('icao_code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('iata_code', models.CharField(max_length=3, unique=True)),
                ('iso_country', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=64)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flt_number', models.CharField(max_length=8)),
                ('callsign', models.CharField(max_length=8)),
                ('acf_type', models.CharField(max_length=8)),
                ('departure_time', models.DateTimeField()),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.airport')),
                ('passengers', models.ManyToManyField(blank=True, to='passenger.passenger')),
                ('pilot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pilot.pilot')),
            ],
        ),
    ]
