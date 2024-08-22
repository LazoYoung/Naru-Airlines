import re
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from flight.models import FlightSchedule, Aircraft, StandardRoute, Airport


# regex_flt_number = re.compile(r'NR\d+')
# regex_flt_time = re.compile(r'[0-1]?[0-9]:[0-5][0-9]')


def aircraft_field(required: bool):
    return serializers.PrimaryKeyRelatedField(
        queryset=Aircraft.objects.all(),
        error_messages={'does_not_exist': _('Aircraft not in our fleet.')},
        required=required,
    )


def airport_field():
    return serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
        error_messages={'does_not_exist': _('Airport not in database.')},
    )


def validate_duration(value):
    if not re.compile(r'[0-1]?[0-9]:[0-5][0-9]').fullmatch(value):
        raise ValidationError("HH:MM is valid format.")


# def validate_callsign(value):
#     if not re.compile(r'[A-Z]{3}\d+').fullmatch(value):
#         raise ValidationError("ICAO code must precede the number.")


class DispatchStandardSerializer(serializers.Serializer):
    flight_number = serializers.IntegerField()
    aircraft = aircraft_field(required=False)
    # callsign = serializers.CharField(validators=[validate_callsign])


class DispatchCharterSerializer(serializers.Serializer):
    # callsign = serializers.CharField(validators=[validate_callsign])
    aircraft = aircraft_field(required=True)
    flight_time = serializers.CharField(validators=[validate_duration])
    departure_time = serializers.DateTimeField()
    departure_airport = airport_field()
    arrival_airport = airport_field()


class FlightScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightSchedule
        exclude = ['pilot']


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class StandardRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardRoute
        fields = '__all__'

    @staticmethod
    def validate_departure_day(value):
        if value < 1 or value > 31:
            raise ValidationError("Day must be between 1 and 31.")
        return value
