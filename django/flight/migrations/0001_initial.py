# Generated by Django 5.0.6 on 2024-09-08 03:42

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pilot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('icao_code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('registration', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(blank=True, upload_to='images/aircraft/')),
            ],
        ),
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
            name='FlightSchedule',
            fields=[
                ('flight_number', models.IntegerField(primary_key=True, serialize=False)),
                ('is_charter', models.BooleanField(default=False)),
                ('departure_time', models.DateTimeField()),
                ('block_time', models.IntegerField()),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.aircraft')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.airport')),
                ('pilot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pilot.pilot')),
            ],
        ),
        migrations.CreateModel(
            name='StandardRoute',
            fields=[
                ('flight_number', models.IntegerField(primary_key=True, serialize=False)),
                ('departure_day', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('departure_zulu', models.TimeField()),
                ('block_time', models.IntegerField()),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.aircraft')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='flight.airport')),
            ],
        ),
    ]
