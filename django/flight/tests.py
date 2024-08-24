import os
import random
import shutil
from datetime import timedelta, time
from time import strptime

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
from scripts.schedule_automation import ScheduleManager
from .models import StandardRoute, FlightSchedule
from .services import DispatcherService
from .utils import create_airport, get_dummy_aircraft, _random_airport_code, create_aircraft, reverse_query

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
        day = self.route1.departure_day
        zulu = self.route1.departure_zulu.isoformat()
        flt_time = str(self.route1.flight_time)
        dep = self.route1.departure_airport.icao_code
        arr = self.route1.arrival_airport.icao_code
        get = self.client.get(reverse("route", kwargs={"flight_number": flt_num}))
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertContains(get, flt_num)
        self.assertContains(get, acf)
        self.assertContains(get, day)
        self.assertContains(get, zulu)
        self.assertContains(get, flt_time)
        self.assertContains(get, dep)
        self.assertContains(get, arr)

    def test_post(self):
        acf = self.aircraft.icao_code
        dep = create_airport()
        arr = create_airport()
        flt_num = self.flight_id
        flt_time = self.random_duration()
        day = self.random_day()
        zulu = self.random_zulu().isoformat()
        post = self.admin.post(
            path=reverse("route"),
            data={
                "flight_number": flt_num,
                "aircraft": acf,
                "departure_day": day,
                "departure_zulu": zulu,
                "flight_time": flt_time,
                "departure_airport": dep.icao_code,
                "arrival_airport": arr.icao_code,
            }
        )
        self.flight_id += 1
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.data["flight_number"], flt_num)
        self.assertEqual(post.data["aircraft"], acf)
        self.assertEqual(post.data["departure_day"], day)
        self.assertEqual(post.data["departure_zulu"], zulu)
        self.assertEqual(post.data["flight_time"], flt_time)
        self.assertEqual(post.data["departure_airport"], dep.icao_code)
        self.assertEqual(post.data["arrival_airport"], arr.icao_code)

    def test_put(self):
        flt_num = self.route1.flight_number
        aircraft = create_aircraft("B748")
        dep = create_airport()
        arr = create_airport()
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

    def _create_route(self):
        route = StandardRoute.objects.create(
            flight_number=self.flight_id,
            aircraft=self.aircraft,
            departure_day=self.random_day(),
            departure_zulu=self.random_zulu(),
            flight_time=self.random_duration(),
            departure_airport=create_airport(),
            arrival_airport=create_airport(),
        )
        self.flight_id += 1
        return route

    @staticmethod
    def _reverse(flight_number):
        return reverse("route", kwargs={"flight_number": flight_number})

    @staticmethod
    def random_day():
        return random.randint(1, 31)

    @staticmethod
    def random_zulu():
        return time(hour=random.randint(0, 23), minute=random.randint(0, 59))

    @staticmethod
    def random_duration():
        hour = random.randint(0, 8)
        minute = random.randint(0, 59)
        return f"{hour}:{minute}"

    @staticmethod
    def to_timedelta(str):
        t = strptime(str, "%H:%M:%S")
        return timedelta(hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec)


class DispatchTest(APITestCase):
    def setUp(self):
        member = Member.objects.create_user(
            handle="pilot",
            display_name="pilot",
            email="pilot_email@test.com",
            password="<PASSWORD>",
        )
        self.pilot = Pilot.objects.create(member=member)
        self.service = DispatcherService(self.pilot)
        self.pilot_client = APIClient()
        self.pilot_client.force_login(member)
        self.aircraft = create_aircraft("B744")
        self.schedule = self._create_schedule()
        # self.route = StandardRoute.objects.create(
        #     flight_number="NR200",
        #     aircraft=self.aircraft,
        #     departure_airport=create_airport(random_airport_code()),
        #     arrival_airport=create_airport(random_airport_code()),
        # )

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
        dispatch = self._dispatch_charter(self.pilot_client)
        self.assertTrue(status.is_success(dispatch.status_code))

    def test_standard(self):
        dispatch = self._dispatch_standard(self.pilot_client)
        self.assertTrue(status.is_success(dispatch.status_code))

    def test_with_invalid_aircraft(self):
        dispatch = self._dispatch_charter(self.pilot_client, data={
            "aircraft": "@@@@"
        })
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("aircraft" in dispatch.data)

    def test_invalid_airport(self):
        departure = create_airport()
        dispatch = self._dispatch_charter(self.pilot_client, data={
            "departure_airport": departure.icao_code,
            "arrival_airport": "@@@@"
        })
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("departure_airport" not in dispatch.data)
        self.assertTrue("arrival_airport" in dispatch.data)

    def test_invalid_flight_number(self):
        dispatch = self._dispatch_standard(self.pilot_client, flight_number=300)
        self.assertTrue(status.is_client_error(dispatch.status_code))
        self.assertTrue("flight_number" in dispatch.data)

    def test_occupied_schedule(self):
        dummy_user = Member.objects.create_user(handle='test', display_name='test', email='<EMAIL>', password='<PASSWORD>')
        dummy_pilot = Pilot.objects.create(member=dummy_user)
        schedule = self._create_schedule(pilot=dummy_pilot)
        dispatch = self._dispatch_standard(
            client=self.pilot_client,
            flight_number=schedule.flight_number
        )
        self.assertTrue(status.is_client_error(dispatch.status_code))


    @staticmethod
    def _dispatch_charter(client, data=None):
        if data is None:
            data = {}
        departure = create_airport()
        arrival = create_airport()
        aircraft = get_dummy_aircraft()
        payload = {
            "aircraft": aircraft.icao_code,
            "flight_time": "1:20",
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
            flight_number = self.schedule.flight_number
        if data is None:
            data = {}
        payload = {
            "flight_number": flight_number,
            "aircraft": self.aircraft.icao_code,
        }
        result = client.post(
            path=reverse('dispatch_standard'),
            data=payload | data,
        )
        return result

    def _create_schedule(self, charter=False, pilot=None):
        flt_number = self.service.available_flight_number(charter=charter)
        self.assertFalse(flt_number is None, "Flight number not available.")
        schedule = FlightSchedule.objects.create(
            flight_number=flt_number,
            flight_time=timedelta(hours=1),
            is_charter=charter,
            pilot=pilot,
            aircraft=self.aircraft,
            departure_time=timezone.now() + timedelta(hours=1),
            departure_airport=create_airport(),
            arrival_airport=create_airport(),
        )
        return schedule


class FlightScheduleTest(TestCase):
    def setUp(self):
        self.schedule_manager = ScheduleManager(test=True)
        self.next_number = 800
        self.aircraft = create_aircraft("A320")

    def test_without_permission(self):
        all = self.client.get(reverse('schedule'))
        mine = self.client.get(reverse_query('schedule', query='mine'))
        available = self.client.get(reverse_query('schedule', query='available'))
        self.assertTrue(status.is_client_error(all.status_code))
        self.assertTrue(status.is_client_error(mine.status_code))
        self.assertTrue(status.is_client_error(available.status_code))

    def test_empty_schedule(self):
        self._create_pilot()
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.data, [])
        self.assertTrue(status.is_success(response.status_code))

    def test_all(self):
        self._create_pilot()

        charter1 = self._dispatch_charter(departure_time=timezone.now() + timezone.timedelta(hours=1))
        charter2 = self._dispatch_charter(departure_time=timezone.now() + timezone.timedelta(hours=2))
        standard1 = self._dispatch_standard(
            schedule=self._standard_schedule(departure_time=timezone.now() + timezone.timedelta(hours=3))
        )
        standard2 = self._dispatch_standard(
            schedule=self._standard_schedule(departure_time=timezone.now() + timezone.timedelta(hours=4))
        )
        flt_number1 = charter1.data['flight_number']
        flt_number2 = charter2.data['flight_number']
        flt_number3 = standard1.data['flight_number']
        flt_number4 = standard2.data['flight_number']

        # Schedules ordered by departure time
        response = self.client.get(reverse('schedule'))
        self.assertTrue(status.is_success(response.status_code))
        data = response.data
        self.assertEqual(flt_number1, data[0]['flight_number'])
        self.assertEqual(flt_number2, data[1]['flight_number'])
        self.assertEqual(flt_number3, data[2]['flight_number'])
        self.assertEqual(flt_number4, data[3]['flight_number'])

        # Correct types
        self.assertTrue(data[0]['is_charter'])
        self.assertTrue(data[1]['is_charter'])
        self.assertFalse(data[2]['is_charter'])
        self.assertFalse(data[3]['is_charter'])

    def test_mine(self):
        self._create_pilot()

        my_schedule = self._dispatch_charter()
        ghost_schedule = self._standard_schedule()
        response = self.client.get(reverse_query('schedule', query='mine'))
        self.assertTrue(status.is_success(response.status_code))
        self.assertContains(response, my_schedule.data['flight_number'])
        self.assertNotContains(response, ghost_schedule.flight_number)

    def test_available(self):
        self._create_pilot()

        schedule1 = self._dispatch_charter()
        schedule2 = self._standard_schedule()
        response = self.client.get(reverse_query('schedule', query='available'))
        self.assertTrue(status.is_success(response.status_code))
        self.assertNotContains(response, schedule1.data['flight_number'])
        self.assertContains(response, schedule2.flight_number)

    def test_get(self):
        self._create_pilot()
        dispatch = self._dispatch_charter()
        flt_number = dispatch.json()['flight_number']
        self.assertTrue(status.is_success(dispatch.status_code))

        get_success = self.client.get(reverse_query('schedule', query={'flight_number': flt_number}))
        self.assertTrue(status.is_success(get_success.status_code))
        self.assertEqual(get_success.data['flight_number'], flt_number)

        # Unknown flight number
        get_fail = self.client.get(reverse_query('schedule', query={'flight_number': 999}))
        self.assertTrue(status.is_client_error(get_fail.status_code))

    def test_delete(self):
        self._create_pilot()
        dispatch = self._dispatch_charter()
        flight_number = dispatch.json()['flight_number']
        self.assertTrue(status.is_success(dispatch.status_code))

        delete = self.client.delete(reverse_query('schedule', query={'flight_number': flight_number}))
        self.assertTrue(status.is_success(delete.status_code))

        delete_fail1 = self.client.delete(reverse_query('schedule', query={'flight_number': 999}))
        self.assertTrue(status.is_client_error(delete_fail1.status_code))

        # The flight does not belong to pilot #2
        self._create_pilot()
        delete_fail2 = self.client.delete(reverse_query('schedule', query={'flight_number': flight_number}))
        self.assertTrue(status.is_client_error(delete_fail2.status_code))

    def _create_pilot(self):
        member = register_and_login(self)
        pilot = Pilot.objects.create(member=member)
        return pilot

    def _standard_schedule(self, flight_number=None, departure_time=timezone.now()):
        if flight_number is None:
            flight_number = self.next_number
            self.next_number += 1
        StandardRoute.objects.create(
            flight_number=flight_number,
            aircraft=self.aircraft,
            flight_time="1:00",
            departure_day=departure_time.day,
            departure_zulu=departure_time.time(),
            departure_airport=create_airport(),
            arrival_airport=create_airport(),
        )
        self.schedule_manager.update_time()
        self.schedule_manager.run()
        schedule = FlightSchedule.objects.filter(flight_number=flight_number).get()
        return schedule

    def _dispatch_charter(self, departure_time=None):
        if departure_time is None:
            departure_time = timezone.now() + timezone.timedelta(hours=1)
        departure = create_airport()
        arrival = create_airport()
        aircraft = self.aircraft
        result = self.client.post(reverse('dispatch_charter'), data={
            "aircraft": aircraft.icao_code,
            "flight_time": "1:20",
            "departure_time": departure_time,
            "departure_airport": departure.icao_code,
            "arrival_airport": arrival.icao_code,
        })
        return result

    def _dispatch_standard(self, schedule: FlightSchedule):
        result = self.client.post(reverse('dispatch_standard'), data={
            "flight_number": schedule.flight_number
        })
        return result
