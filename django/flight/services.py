from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from flight.models import Aircraft, FlightSchedule, Airport


class DispatchError(Exception):
    def __init__(self, reason, error_key=None, bad_request=False):
        self.reason = reason
        self.bad_request = bad_request
        self.error_key = error_key if error_key else "errors"

    @property
    def status(self):
        if self.bad_request:
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_500_INTERNAL_SERVER_ERROR

    def response(self):
        return Response(data={self.error_key: self.reason}, status=self.status)


@dataclass
class RoutineDTO:
    flight_number: int
    aircraft: Optional[Aircraft]


@dataclass
class CharterDTO:
    aircraft: Aircraft
    block_time: int
    departure_time: datetime
    departure_airport: Airport
    arrival_airport: Airport


class DispatcherService(object):
    standard_numbers = set(range(100, 300))
    charter_numbers = set(range(300, 400))

    def __init__(self, pilot):
        self.pilot = pilot

    def dispatch_charter(self, dto: CharterDTO) -> FlightSchedule:
        flight_number = self.available_flight_number()

        if flight_number is None:
            raise DispatchError("Charter service is full! Try again later.")

        try:
            return FlightSchedule.objects.create(
                flight_number=flight_number,
                is_charter=True,
                pilot=self.pilot,
                aircraft=dto.aircraft,
                block_time=dto.block_time,
                departure_time=dto.departure_time,
                departure_airport=dto.departure_airport,
                arrival_airport=dto.arrival_airport,
            )
        except IntegrityError:
            return self.dispatch_charter(dto)

    def dispatch_routine(self, dto: RoutineDTO) -> FlightSchedule:
        query = FlightSchedule.objects.filter(flight_number=dto.flight_number)

        if not query.exists():
            raise DispatchError("Invalid flight number.", error_key="flight_number", bad_request=True)

        schedule = query.get()

        if schedule.is_charter:
            raise DispatchError("This is a charter flight.", bad_request=True)

        if schedule.pilot:
            raise DispatchError("This flight is occupied.", bad_request=True)

        if dto.aircraft:
            schedule.aircraft = dto.aircraft

        schedule.pilot = self.pilot
        schedule.save()
        return schedule

    def available_flight_number(self, charter=True):
        used_numbers = (
            FlightSchedule
            .objects
            .values_list('flight_number', flat=True)
            .order_by('flight_number')
        )
        all_numbers = self.charter_numbers if charter else self.standard_numbers
        available_numbers = all_numbers - set(used_numbers)

        if len(available_numbers) > 0:
            return list(available_numbers)[0]
        else:
            return None
