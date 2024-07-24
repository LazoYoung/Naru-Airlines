import random
import string

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from member.tests import register_and_login
from pilot.models import Pilot
from .models import Airport


class DispatchTest(TestCase):
    def test_as_guest(self):
        dispatch = self._dispatch()
        self.assertTrue(status.is_client_error(dispatch.status_code))

    def test_as_member(self):
        register_and_login(self)

        dispatch = self._dispatch()
        self.assertTrue(status.is_client_error(dispatch.status_code))

    def test_as_pilot(self):
        member = register_and_login(self)
        Pilot.objects.create(member=member)

        dispatch = self._dispatch()
        self.assertTrue(status.is_success(dispatch.status_code))

    def test_with_invalid_airport(self):
        member = register_and_login(self)
        Pilot.objects.create(member=member)

        departure = create_airport("Departure airport")
        dispatch = self.client.post(reverse('dispatch'), data={
            "flt_number": "NR234",
            "callsign": "NAR234",
            "acf_type": "A320",
            "departure_time": timezone.now() + timezone.timedelta(hours=1),
            "departure_airport": departure.icao_code,
            "arrival_airport": 'AAAA',
        })
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("departure_airport" not in dispatch.data)
        self.assertTrue("arrival_airport" in dispatch.data)

    def _dispatch(self):
        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        result = self.client.post(reverse('dispatch'), data={
            "flt_number": "NR234",
            "callsign": "NAR234",
            "acf_type": "A320",
            "departure_time": timezone.now() + timezone.timedelta(hours=1),
            "departure_airport": departure.icao_code,
            "arrival_airport": arrival.icao_code,
        })
        return result


class FlightScheduleTest(TestCase):
    def test_schedules_without_permission(self):
        no_perm = self.client.get(reverse('schedules'))
        self.assertTrue(status.is_client_error(no_perm.status_code))

    def test_schedules(self):
        self._create_pilot()

        empty_schedule = self.client.get(reverse('schedules'))
        self.assertEqual(empty_schedule.data, [])
        self.assertTrue(status.is_success(empty_schedule.status_code))

        flt_number1 = "NR001"
        flt_number2 = "NR002"
        dispatch1 = self._dispatch(flt_number=flt_number1)
        dispatch2 = self._dispatch(flt_number=flt_number2)
        self.assertTrue(status.is_success(dispatch1.status_code))
        self.assertTrue(status.is_success(dispatch2.status_code))

        schedules = self.client.get(reverse('schedules'))
        self.assertTrue(status.is_success(schedules.status_code))
        self.assertContains(schedules, text=flt_number1, count=1)
        self.assertContains(schedules, text=flt_number2, count=1)

        # New pilot has empty schedule
        self._create_pilot()
        empty_schedule = self.client.get(reverse('schedules'))
        self.assertEqual(empty_schedule.data, [])
        self.assertTrue(status.is_success(empty_schedule.status_code))

    def test_get_flight(self):
        flt_number = "NR003"

        self._create_pilot()
        dispatch = self._dispatch(flt_number=flt_number)
        self.assertTrue(status.is_success(dispatch.status_code))

        get_success = self.client.get(reverse('schedule', args=[flt_number]))
        self.assertTrue(status.is_success(get_success.status_code))
        self.assertEqual(get_success.data['flt_number'], flt_number)

        # Unknown flight number
        get_fail = self.client.get(reverse('schedule', args=["NR999"]))
        self.assertTrue(status.is_client_error(get_fail.status_code))

    def test_put_flight(self):
        flt_number1 = "NR004"
        flt_number2 = "NR005"

        self._create_pilot()
        dispatch1 = self._dispatch(flt_number=flt_number1)
        self.assertTrue(status.is_success(dispatch1.status_code))

        put_success1 = self.client.put(
            path=reverse('schedule', args=[flt_number1]),
            content_type='application/json',
            data={"callsign": "NAR123"}
        )
        self.assertTrue(status.is_success(put_success1.status_code))

        self._create_pilot()
        dispatch2 = self._dispatch(flt_number=flt_number2)
        self.assertTrue(status.is_success(dispatch2.status_code))

        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        put_success2 = self.client.put(
            path=reverse('schedule', args=[flt_number2]),
            content_type='application/json',
            data={
                "callsign": "NAR345",
                "acf_type": "A320",
                "departure_time": timezone.now() + timezone.timedelta(hours=2),
                "departure_airport": departure.icao_code,
                "arrival_airport": arrival.icao_code,
            }
        )
        self.assertTrue(status.is_success(put_success2.status_code))

        # flt_number1 does not belong to pilot #2
        put_fail1 = self.client.put(
            path=reverse('schedule', args=[flt_number1]),
            content_type='application/json',
            data={
                "callsign": "NAR456"
            }
        )
        self.assertTrue(status.is_client_error(put_fail1.status_code))

        # Field `flt_number` is immutable.
        put_fail2 = self.client.put(
            path=reverse('schedule', args=[flt_number2]),
            content_type='application/json',
            data={
                "flt_number": "NR567"
            }
        )
        self.assertTrue(status.is_client_error(put_fail2.status_code))
        self.assertTrue('flt_number' in put_fail2.data)

    def test_delete_flight(self):
        flt_number = "NR007"

        self._create_pilot()
        dispatch = self._dispatch(flt_number=flt_number)
        self.assertTrue(status.is_success(dispatch.status_code))

        delete = self.client.delete(reverse('schedule', args=[flt_number]))
        self.assertTrue(status.is_success(delete.status_code))

        delete_fail1 = self.client.delete(reverse('schedule', args=["NR999"]))
        self.assertTrue(status.is_client_error(delete_fail1.status_code))

        # The flight does not belong to pilot #2
        self._create_pilot()
        delete_fail2 = self.client.delete(reverse('schedule', args=[flt_number]))
        self.assertTrue(status.is_client_error(delete_fail2.status_code))

    def _create_pilot(self):
        member = register_and_login(self)
        pilot = Pilot.objects.create(member=member)
        return pilot

    def _dispatch(self, flt_number):
        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        result = self.client.post(reverse('dispatch'), data={
            "flt_number": flt_number,
            "callsign": "NAR234",
            "acf_type": "A320",
            "departure_time": timezone.now() + timezone.timedelta(hours=1),
            "departure_airport": departure.icao_code,
            "arrival_airport": arrival.icao_code,
        })
        return result


def create_airport(name):
    return Airport.objects.create(
        name=name,
        icao_code=random_airport_code(True),
        iata_code=random_airport_code(False),
        iso_country="KR",
        city="Seoul",
        latitude="0.0",
        longitude="0.0",
    )


def random_airport_code(icao=True):
    length = 4 if icao else 3
    field = 'icao_code' if icao else 'iata_code'
    while True:
        seq = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(seq) for _ in range(length))
        if code not in Airport.objects.values_list(field, flat=True):
            return code
