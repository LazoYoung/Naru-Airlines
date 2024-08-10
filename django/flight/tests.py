import random
import string

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from member.models import Member
from member.tests import register_and_login
from pilot.models import Pilot
from .models import Airport, Aircraft


class FleetTest(APITestCase):
    admin = None

    def setUp(self):
        self.admin = Member.objects.create_superuser(handle="admin", display_name="admin", email="<EMAIL>", password="<PASSWORD>")

    def test_fleet_all(self):
        self._create_aircraft("A320")
        self._create_aircraft("B738")
        response = self.client.get(reverse("fleet_all"))
        self.assertContains(response, "A320")
        self.assertContains(response, "B738")

    def test_fleet_get(self):
        aircraft1 = self._create_aircraft("A320")
        aircraft2 = self._create_aircraft("B738")
        icao_code1 = aircraft1.icao_code
        icao_code2 = aircraft2.icao_code
        response1 = self.client.get(self._reverse(icao_code1))
        response2 = self.client.get(self._reverse(icao_code2))
        self.assertContains(response1, icao_code1)
        self.assertContains(response2, icao_code2)

    def test_without_permission(self):
        self.client.logout()
        response = self.client.post(
            reverse("fleet_aircraft", kwargs={"icao_code": "A320"}),
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fleet_crud(self):
        icao_code = "B748"
        client = APIClient()
        client.force_login(self.admin)

        post = client.post(
            path=reverse("fleet_aircraft"),
            data={
                "icao_code": icao_code,
                "registration": "HL5678",
                "name": "Boeing 747-8i"
            }
        )
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        post = client.get(self._reverse(icao_code))
        self.assertContains(post, icao_code)

        new_reg = "HL9999"
        new_name = "Queen of the Sky"
        bad_file = SimpleUploadedFile(
            name="wav_file.wav",
            content=b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04\x00\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00',
            content_type='audio/wav',
        )
        bad_put = client.put(
            path=self._reverse(icao_code),
            data={
                "registration": new_reg,
                "name": new_name,
                "image": bad_file
            },
        )
        self.assertEqual(bad_put.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("image" in bad_put.json())

        put = client.put(
            path=self._reverse(icao_code),
            data={
                "registration": new_reg,
                "name": new_name,
                # todo: embed real image
            }
        )
        self.assertEqual(put.status_code, status.HTTP_204_NO_CONTENT)
        put = client.get(self._reverse(icao_code))
        self.assertContains(put, new_reg)
        self.assertContains(put, new_name)

        delete = client.delete(self._reverse(icao_code))
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)

        client.logout()

    @staticmethod
    def _reverse(icao_code):
        return reverse("fleet_aircraft", kwargs={"icao_code": icao_code})

    @staticmethod
    def _create_aircraft(icao_code):
        return Aircraft.objects.create(
            icao_code=icao_code,
            registration="HL1111",
            name="Random aircraft",
        )


class DispatchCharterTest(TestCase):
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
        aircraft = get_dummy_aircraft()
        dispatch = self.client.post(reverse('dispatch_charter'), data={
            "flight_number": "NR234",
            "flight_time": "1:20",
            "callsign": "NAR234",
            "aircraft": aircraft.icao_code,
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
        aircraft = get_dummy_aircraft()
        result = self.client.post(reverse('dispatch_charter'), data={
            "flight_number": "NR234",
            "flight_time": "1:20",
            "callsign": "NAR234",
            "aircraft": aircraft.icao_code,
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

        response = self.client.get(reverse('schedules'))
        self.assertEqual(response.data, [])
        self.assertTrue(status.is_success(response.status_code))

        flt_number1 = "NR001"
        flt_number2 = "NR002"
        flt_number3 = "NR003"
        dispatch1 = self._dispatch_charter(
            flt_number=flt_number1,
            departure_time=timezone.now() + timezone.timedelta(hours=1)
        )
        dispatch2 = self._dispatch_charter(
            flt_number=flt_number2,
            departure_time=timezone.now() + timezone.timedelta(hours=2)
        )
        dispatch3 = self._dispatch_charter(
            flt_number=flt_number3,
            departure_time=timezone.now() + timezone.timedelta(hours=3)
        )
        self.assertTrue(status.is_success(dispatch1.status_code))
        self.assertTrue(status.is_success(dispatch2.status_code))
        self.assertTrue(status.is_success(dispatch3.status_code))

        # Schedules ordered by departure time (asc)
        response = self.client.get(reverse('schedules'))
        self.assertTrue(status.is_success(response.status_code))
        schedules = response.data
        self.assertEqual(flt_number1, schedules[0]['flight_number'])
        self.assertEqual(flt_number2, schedules[1]['flight_number'])
        self.assertEqual(flt_number3, schedules[2]['flight_number'])

        # New pilot has empty schedule
        self._create_pilot()
        response = self.client.get(reverse('schedules'))
        self.assertEqual(response.data, [])
        self.assertTrue(status.is_success(response.status_code))

    def test_get_flight(self):
        flt_number = "NR003"

        self._create_pilot()
        dispatch = self._dispatch_charter(flt_number=flt_number)
        self.assertTrue(status.is_success(dispatch.status_code))

        get_success = self.client.get(reverse('schedule', args=[flt_number]))
        self.assertTrue(status.is_success(get_success.status_code))
        self.assertEqual(get_success.data['flight_number'], flt_number)

        # Unknown flight number
        get_fail = self.client.get(reverse('schedule', args=["NR999"]))
        self.assertTrue(status.is_client_error(get_fail.status_code))

    def test_put_flight(self):
        flt_number1 = "NR004"
        flt_number2 = "NR005"

        self._create_pilot()
        dispatch1 = self._dispatch_charter(flt_number=flt_number1)
        self.assertTrue(status.is_success(dispatch1.status_code))

        put_success1 = self.client.put(
            path=reverse('schedule', args=[flt_number1]),
            content_type='application/json',
            data={"callsign": "NAR123"}
        )
        self.assertTrue(status.is_success(put_success1.status_code))

        self._create_pilot()
        dispatch2 = self._dispatch_charter(flt_number=flt_number2)
        self.assertTrue(status.is_success(dispatch2.status_code))

        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        aircraft = get_dummy_aircraft()
        put_success2 = self.client.put(
            path=reverse('schedule', args=[flt_number2]),
            content_type='application/json',
            data={
                "callsign": "NAR345",
                "aircraft": aircraft.icao_code,
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
                "flight_number": "NR567"
            }
        )
        self.assertTrue(status.is_client_error(put_fail2.status_code))
        self.assertTrue('flight_number' in put_fail2.data)

    def test_delete_flight(self):
        flight_number = "NR007"

        self._create_pilot()
        dispatch = self._dispatch_charter(flt_number=flight_number)
        self.assertTrue(status.is_success(dispatch.status_code))

        delete = self.client.delete(reverse('schedule', args=[flight_number]))
        self.assertTrue(status.is_success(delete.status_code))

        delete_fail1 = self.client.delete(reverse('schedule', args=["NR999"]))
        self.assertTrue(status.is_client_error(delete_fail1.status_code))

        # The flight does not belong to pilot #2
        self._create_pilot()
        delete_fail2 = self.client.delete(reverse('schedule', args=[flight_number]))
        self.assertTrue(status.is_client_error(delete_fail2.status_code))

    def _create_pilot(self):
        member = register_and_login(self)
        pilot = Pilot.objects.create(member=member)
        return pilot

    def _dispatch_charter(self, flt_number, departure_time=None):
        if departure_time is None:
            departure_time = timezone.now() + timezone.timedelta(hours=1)
        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        aircraft = get_dummy_aircraft()
        result = self.client.post(reverse('dispatch_charter'), data={
            "flight_number": flt_number,
            "flight_time": "1:20",
            "callsign": "NAR234",
            "aircraft": aircraft.icao_code,
            "departure_time": departure_time,
            "departure_airport": departure.icao_code,
            "arrival_airport": arrival.icao_code,
        })
        return result


def get_dummy_aircraft():
    return Aircraft.objects.get_or_create(
        icao_code="A320",
        defaults={
            "registration": "HL1234",
            "name": "Airbus A320 IAE",
        }
    )[0]


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
