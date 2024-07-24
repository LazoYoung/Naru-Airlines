import re

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from flight.models import Flight
from pilot.models import Pilot

regex_flt_number = re.compile(r'NR\d+')
regex_callsign = re.compile(r'[A-Z]{3}\d+')


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        # fields = '__all__'
        exclude = ['pilot']

    @staticmethod
    def validate_flt_number(value):
        if not regex_flt_number.fullmatch(value):
            raise ValidationError("It must begin with prefix NR.")
        return value

    @staticmethod
    def validate_callsign(value):
        if not regex_callsign.fullmatch(value):
            raise ValidationError("Invalid callsign.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            pilot = Pilot.objects.get(member=user)
        except ObjectDoesNotExist:
            raise ValidationError("Pilot record missing.")

        return Flight.objects.create(
            pilot=pilot,
            flt_number=validated_data['flt_number'],
            callsign=validated_data['callsign'],
            acf_type=validated_data['acf_type'],
            departure_time=validated_data['departure_time'],
            departure_airport=validated_data['departure_airport'],
            arrival_airport=validated_data['arrival_airport'],
        )

    def update(self, instance, validated_data):
        if 'flt_number' in validated_data:
            raise ValidationError({"flt_number": "This field cannot be updated."})

        instance.callsign = validated_data.get('callsign', instance.callsign)
        instance.acf_type = validated_data.get('acf_type', instance.acf_type)
        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.departure_airport = validated_data.get('departure_airport', instance.departure_airport)
        instance.arrival_airport = validated_data.get('arrival_airport', instance.arrival_airport)
        instance.save()

        return instance
