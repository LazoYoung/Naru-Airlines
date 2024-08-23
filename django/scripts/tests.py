from datetime import time, datetime, tzinfo, timezone

from django.test import TestCase

from flight.models import StandardRoute, FlightSchedule
from flight.utils import create_aircraft, create_airport
from scripts.schedule_automation import ScheduleManager


class ScheduleAutomationTest(TestCase):
    def setUp(self):
        self.manager = ScheduleManager(test=True)
        self.acf = create_aircraft("B738")
        self.dep = create_airport()
        self.arr = create_airport()
        self.next_number = 900

    def _create_route(self, day: int, zulu: time):
        # zulu = zulu.replace(tzinfo=timezone.utc)
        route = StandardRoute.objects.create(
            flight_number=self.next_number,
            aircraft=self.acf,
            departure_day=day,
            departure_zulu=zulu,
            flight_time="1:00",
            departure_airport=self.dep,
            arrival_airport=self.arr,
        )
        self.next_number += 1
        return route

    def test_script(self):
        route1 = self._create_route(day=1, zulu=time(hour=9))
        route2 = self._create_route(day=30, zulu=time(hour=9))
        self.manager.update_time(time=datetime(2024, 12, 25))
        self.manager.run()

        query1 = FlightSchedule.objects.filter(flight_number=route1.flight_number)
        query2 = FlightSchedule.objects.filter(flight_number=route2.flight_number)
        self.assertTrue(query1.exists())
        self.assertTrue(query2.exists())

        schedule1 = query1.get()
        schedule2 = query2.get()
        self.assertEqual(schedule1.departure_time.year, 2025)
        self.assertEqual(schedule1.departure_time.month, 1)
        self.assertEqual(schedule2.departure_time.year, 2024)
        self.assertEqual(schedule2.departure_time.month, 12)
