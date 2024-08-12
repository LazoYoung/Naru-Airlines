import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from flight.models import Flight, Aircraft, StandardRoute, Airport
from pilot.models import Pilot

regex_flt_number = re.compile(r'NR\d+')
regex_flt_time = re.compile(r'[0-1]?[0-9]:[0-5][0-9]')
regex_callsign = re.compile(r'[A-Z]{3}\d+')


class FlightSerializer(serializers.ModelSerializer):
    aircraft = serializers.PrimaryKeyRelatedField(
        queryset=Aircraft.objects.all(),
        error_messages={'does_not_exist': _('Aircraft not in our fleet.')}
    )
    departure_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
        error_messages={'does_not_exist': _('Airport not in database.')}
    )
    arrival_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
        error_messages={'does_not_exist': _('Airport not in database.')}
    )

    class Meta:
        model = Flight
        exclude = ['pilot']

    @staticmethod
    def validate_flight_number(value):
        if not regex_flt_number.fullmatch(value):
            raise ValidationError("Flight number must start with: NR")
        return value

    @staticmethod
    def validate_flight_time(value):
        if not regex_flt_time.fullmatch(value):
            raise ValidationError("HH:MM is the right form to represent time.")
        return value

    @staticmethod
    def validate_callsign(value):
        if not regex_callsign.fullmatch(value):
            raise ValidationError("ICAO code must precede the number.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            pilot = Pilot.objects.get(member=user)
        except ObjectDoesNotExist:
            raise ValidationError("Pilot record missing.")

        return Flight.objects.create(
            pilot=pilot,
            flight_number=validated_data['flight_number'],
            flight_time=validated_data['flight_time'],
            callsign=validated_data['callsign'],
            aircraft=validated_data['aircraft'],
            departure_time=validated_data['departure_time'],
            departure_airport=validated_data['departure_airport'],
            arrival_airport=validated_data['arrival_airport'],
        )

    def update(self, instance, validated_data):
        if 'flight_number' in validated_data:
            raise ValidationError({"flight_number": "This field cannot be updated."})

        instance.flight_time = validated_data.get('flight_time', instance.flight_time)
        instance.callsign = validated_data.get('callsign', instance.callsign)
        instance.aircraft = validated_data.get('aircraft', instance.aircraft)
        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.departure_airport = validated_data.get('departure_airport', instance.departure_airport)
        instance.arrival_airport = validated_data.get('arrival_airport', instance.arrival_airport)
        instance.save()

        return instance


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class StandardRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardRoute
        fields = '__all__'

    @staticmethod
    def validate_flight_number(value):
        if not regex_flt_number.fullmatch(value):
            raise ValidationError("Prefix 'NR' must precede the number.")
        return value
