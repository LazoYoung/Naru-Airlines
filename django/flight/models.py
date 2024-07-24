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


class Flight(models.Model):
    class Phase(models.IntegerChoices):
        PREFLIGHT = 0
        BOARDING = 1
        DEPARTING = 2
        CRUISING = 3
        LANDED = 4
        ARRIVED = 5

    flt_number = models.CharField(max_length=8, primary_key=True)
    phase = models.IntegerField(choices=Phase, default=Phase.PREFLIGHT)
    pilot = models.ForeignKey(Pilot, on_delete=models.SET_NULL, null=True)
    passengers = models.ManyToManyField(Passenger, blank=True)
    callsign = models.CharField(max_length=8)
    acf_type = models.CharField(max_length=8)
    departure_time = models.DateTimeField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='+')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='+')
