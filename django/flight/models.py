from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from passenger.models import Passenger
from pilot.models import Pilot


class Airport(models.Model):
    icao_code = models.CharField(max_length=4, primary_key=True)
    iata_code = models.CharField(max_length=3, unique=True)
    iso_country = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Aircraft(models.Model):
    icao_code = models.CharField(max_length=4, primary_key=True)
    registration = models.CharField(max_length=8)
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to="images/aircraft/", blank=True)


class FlightSchedule(models.Model):
    flight_number = models.IntegerField(primary_key=True)
    is_charter = models.BooleanField(default=False)
    pilot = models.ForeignKey(Pilot, on_delete=models.SET_NULL, null=True)
    flight_time = models.CharField(max_length=5)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT, related_name='+')
    departure_time = models.DateTimeField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='+')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='+')


class StandardRoute(models.Model):
    flight_number = models.IntegerField(primary_key=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT, related_name='+')
    departure_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    departure_zulu = models.TimeField()
    flight_time = models.CharField(max_length=5)
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='+')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='+')
