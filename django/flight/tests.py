import os
import random
import shutil
import string

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from member.models import Member
from member.tests import register_and_login
from pilot.models import Pilot
from .models import Airport, Aircraft, StandardRoute

# temporary media folder
TEST_DIR = settings.BASE_DIR / 'test_media'


@override_settings(MEDIA_ROOT=TEST_DIR)
class FleetTest(APITestCase):
    def setUp(self):
        os.mkdir(TEST_DIR)
        superuser = Member.objects.create_superuser(
            handle="admin",
            display_name="admin",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.admin = APIClient()
        self.admin.force_login(superuser)

    def test_fleet_all(self):
        create_aircraft("A320")
        create_aircraft("B738")
        response = self.client.get(reverse("fleet_profiles"))
        self.assertContains(response, "A320")
        self.assertContains(response, "B738")

    def test_fleet_get(self):
        aircraft1 = create_aircraft("A320")
        aircraft2 = create_aircraft("B738")
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
        icao_code = "A320"

        post = self.admin.post(
            path=reverse("fleet_aircraft"),
            data={
                "icao_code": icao_code,
                "registration": "HL5678",
                "name": "Boeing 747-8i",
                "image": self._image(),
            }
        )
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        post = self.admin.get(self._reverse(icao_code))
        self.assertContains(post, icao_code)

        new_reg = "HL9999"
        new_name = "Airbus A320 CFM"
        bad_file = SimpleUploadedFile(
            name="wav_file.wav",
            content=b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04\x00\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00',
            content_type='audio/wav',
        )
        bad_put = self.admin.put(
            path=self._reverse(icao_code),
            data={
                "registration": new_reg,
                "name": new_name,
                "image": bad_file,
            },
        )
        self.assertEqual(bad_put.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("image" in bad_put.json())

        put = self.admin.put(
            path=self._reverse(icao_code),
            data={
                "registration": new_reg,
                "name": new_name,
                "image": self._image(),
            }
        )
        self.assertEqual(put.status_code, status.HTTP_204_NO_CONTENT)
        put = self.admin.get(self._reverse(icao_code))
        self.assertContains(put, new_reg)
        self.assertContains(put, new_name)

        delete = self.admin.delete(self._reverse(icao_code))
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError as e:
            print("Failed to delete temporary files:", e)

    @staticmethod
    def _reverse(icao_code):
        return reverse("fleet_aircraft", kwargs={"icao_code": icao_code})

    @staticmethod
    def _image():
        file_name = "a320.png"
        with open(finders.find(file_name), 'rb') as file:
            bytes = file.read()
            image_file = SimpleUploadedFile(
                name=file_name,
                content=bytes,
                content_type="image/png"
            )
            return image_file


class StandardRouteTests(APITestCase):
    def setUp(self):
        self.superuser = Member.objects.create_superuser(
            handle="admin",
            display_name="admin",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        self.admin = APIClient()
        self.admin.force_login(self.superuser)
        self.flight_id = 100
        self.aircraft = create_aircraft("A320")
        self.route1 = self._create_route()
        self.route2 = self._create_route()
        self.route3 = self._create_route()

    def test_routes(self):
        response = self.client.get(reverse("routes"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.route1.flight_number)
        self.assertContains(response, self.route2.flight_number)
        self.assertContains(response, self.route3.flight_number)

    def test_get(self):
        flt_num = self.route1.flight_number
        acf = self.route1.aircraft.icao_code
        dep = self.route1.departure_airport.icao_code
        arr = self.route1.arrival_airport.icao_code
        get = self.client.get(reverse("route", kwargs={"flight_number": flt_num}))
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertContains(get, flt_num)
        self.assertContains(get, acf)
        self.assertContains(get, dep)
        self.assertContains(get, arr)

    def test_post(self):
        dep = create_airport(random_airport_code())
        arr = create_airport(random_airport_code())
        flt_num = self._flight_number()
        post = self.admin.post(
            path=reverse("route"),
            data={
                "flight_number": flt_num,
                "aircraft": self.aircraft.icao_code,
                "departure_airport": dep.icao_code,
                "arrival_airport": arr.icao_code,
            }
        )
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.data["flight_number"], flt_num)
        self.assertEqual(post.data["aircraft"], self.aircraft.icao_code)
        self.assertEqual(post.data["departure_airport"], dep.icao_code)
        self.assertEqual(post.data["arrival_airport"], arr.icao_code)

    def test_put(self):
        flt_num = self.route1.flight_number
        aircraft = create_aircraft("B748")
        dep = create_airport(random_airport_code())
        arr = create_airport(random_airport_code())
        put = self.admin.put(
            path=self._reverse(flight_number=flt_num),
            data={
                "aircraft": aircraft.icao_code,
                "departure_airport": dep.icao_code,
                "arrival_airport": arr.icao_code,
            }
        )
        self.assertEqual(put.status_code, status.HTTP_204_NO_CONTENT)
        get = self.client.get(self._reverse(flt_num))
        self.assertContains(get, aircraft.icao_code)
        self.assertContains(get, dep.icao_code)
        self.assertContains(get, arr.icao_code)

    def test_delete(self):
        flt_num = self.route2.flight_number
        delete = self.admin.delete(self._reverse(flt_num))
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
        get = self.client.get(self._reverse(flt_num))
        self.assertEqual(get.status_code, status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _reverse(flight_number):
        return reverse("route", kwargs={"flight_number": flight_number})

    def _create_route(self):
        route = StandardRoute.objects.create(
            flight_number=self._flight_number(),
            aircraft=self.aircraft,
            departure_airport=create_airport(random_airport_code()),
            arrival_airport=create_airport(random_airport_code()),
        )
        return route

    def _flight_number(self):
        flt_num = f"NR{self.flight_id}"
        self.flight_id += 1
        return flt_num


class DispatchTest(APITestCase):
    def setUp(self):
        member = Member.objects.create_user(
            handle="pilot",
            display_name="pilot",
            email="<EMAIL>",
            password="<PASSWORD>",
        )
        Pilot.objects.create(member=member)
        self.pilot = APIClient()
        self.pilot.force_login(member)
        self.aircraft = create_aircraft("B744")
        self.route = StandardRoute.objects.create(
            flight_number="NR200",
            aircraft=self.aircraft,
            departure_airport=create_airport(random_airport_code()),
            arrival_airport=create_airport(random_airport_code()),
        )

    def test_without_permission(self):
        # try as guest
        charter = self._dispatch_charter(self.client)
        standard = self._dispatch_standard(self.client)
        self.assertTrue(status.is_client_error(charter.status_code))
        self.assertTrue(status.is_client_error(standard.status_code))

        # try as member (non-pilot)
        register_and_login(self)
        charter = self._dispatch_charter(self.client)
        standard = self._dispatch_standard(self.client)
        self.assertTrue(status.is_client_error(charter.status_code))
        self.assertTrue(status.is_client_error(standard.status_code))

    def test_charter(self):
        dispatch = self._dispatch_charter(self.pilot)
        self.assertTrue(status.is_success(dispatch.status_code))

    def test_standard(self):
        dispatch = self._dispatch_standard(self.pilot)
        self.assertTrue(status.is_success(dispatch.status_code))

    def test_with_invalid_aircraft(self):
        dispatch = self._dispatch_charter(self.pilot, data={
            "aircraft": "@@@@"
        })
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("aircraft" in dispatch.data)

    def test_with_invalid_airport(self):
        departure = create_airport("Departure airport")
        dispatch = self._dispatch_charter(self.pilot, data={
            "departure_airport": departure.icao_code,
            "arrival_airport": "@@@@"
        })
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("departure_airport" not in dispatch.data)
        self.assertTrue("arrival_airport" in dispatch.data)

    def test_with_invalid_flight_number(self):
        StandardRoute.objects.create(
            flight_number="NR999",
            aircraft=self.aircraft,
            departure_airport=create_airport(random_airport_code()),
            arrival_airport=create_airport(random_airport_code()),
        )
        dispatch = self._dispatch_standard(self.pilot, flight_number="NR111")
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("flight_number" in dispatch.data)

    @staticmethod
    def _dispatch_charter(client, data=None):
        if data is None:
            data = {}
        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        aircraft = get_dummy_aircraft()
        payload = {
            "flight_number": "NR234",
            "flight_time": "1:20",
            "callsign": "NAR234",
            "aircraft": aircraft.icao_code,
            "departure_time": timezone.now() + timezone.timedelta(hours=1),
            "departure_airport": departure.icao_code,
            "arrival_airport": arrival.icao_code,
        }
        result = client.post(
            path=reverse('dispatch_charter'),
            data=payload | data
        )
        return result

    def _dispatch_standard(self, client, flight_number=None, data=None):
        if flight_number is None:
            flight_number = self.route.flight_number
        if data is None:
            data = {}
        payload = {
            "flight_number": flight_number,
            "callsign": "NAR560",
            "flight_time": "1:30",
            "departure_time": timezone.now() + timezone.timedelta(hours=1),
        }
        result = client.post(
            path=reverse('dispatch_standard'),
            data=payload | data,
        )
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


def create_aircraft(icao_code) -> Aircraft:
    return Aircraft.objects.create(
        icao_code=icao_code,
        registration="HL1111",
        name="Random aircraft",
    )


def random_airport_code(icao=True):
    length = 4 if icao else 3
    field = 'icao_code' if icao else 'iata_code'
    while True:
        seq = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(seq) for _ in range(length))
        if code not in Airport.objects.values_list(field, flat=True):
            return code
