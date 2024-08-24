from datetime import datetime, timezone as tz, tzinfo

from django.db import IntegrityError
from django.utils import timezone
from tqdm import tqdm

from flight.models import StandardRoute, FlightSchedule


class ScheduleManager:
    def __init__(self, test=False):
        self.count = 0
        self.skip = 0
        self._now = timezone.now()
        self._test = test

    def update_time(self, time=timezone.now()):
        self._now = time

    def run(self):
        self.count = 0
        self.skip = 0
        used_numbers = FlightSchedule.objects.values_list('flight_number', flat=True)
        routes = StandardRoute.objects.exclude(flight_number__in=used_numbers)

        if self._test:
            for route in routes:
                self._add_schedule(route)
            return

        for route in tqdm(routes, total=routes.count()):
            self._add_schedule(route)

        if self.skip:
            print(f"{self.skip} items were skipped.")

        if self.count:
            print(f"{self.count} schedules were created.")
        else:
            print("No schedules were created.")

    def _add_schedule(self, route: StandardRoute):
        zulu = route.departure_zulu
        year = self._now.year

        if self._now.day < route.departure_day:
            month = self._now.month
        elif self._now.month < 12:
            month = self._now.month + 1
        else:
            year += 1
            month = 1

        departure_time = datetime(
            year=year,
            month=month,
            day=route.departure_day,
            hour=zulu.hour,
            minute=zulu.minute,
            tzinfo=tz.utc,
        )

        try:
            FlightSchedule.objects.create(
                flight_number=route.flight_number,
                is_charter=False,
                flight_time=route.flight_time,
                aircraft=route.aircraft,
                departure_time=departure_time,
                departure_airport=route.departure_airport,
                arrival_airport=route.arrival_airport,
            )
            self.count += 1
        except IntegrityError as err:
            print(err)
            self.skip += 1


manager = ScheduleManager()


def run():
    manager.update_time()
    manager.run()
