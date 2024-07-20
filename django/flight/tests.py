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
    def dispatch(self):
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

    def test_as_guest(self):
        dispatch = self.dispatch()
        self.assertTrue(status.is_client_error(dispatch.status_code))

    def test_as_member(self):
        register_and_login(self)

        dispatch = self.dispatch()
        self.assertTrue(status.is_client_error(dispatch.status_code))

    def test_as_pilot(self):
        member = register_and_login(self)
        Pilot.objects.create(member=member)

        dispatch = self.dispatch()
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


class FlightViewTest(TestCase):
    def authenticate(self):
        member = register_and_login(self)
        Pilot.objects.create(member=member)

    def dispatch(self, flt_number):
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

    def test_list_without_permission(self):
        response = self.client.get(reverse('flight_list'))
        self.assertTrue(status.is_client_error(response.status_code))

    def test_list_without_flights(self):
        self.authenticate()
        response = self.client.get(reverse('flight_list'))
        self.assertEqual(response.data, [])
        self.assertTrue(status.is_success(response.status_code))

    def test_list(self):
        flt_number1 = "NR001"
        flt_number2 = "NR002"

        self.authenticate()
        dispatch1 = self.dispatch(flt_number=flt_number1)
        dispatch2 = self.dispatch(flt_number=flt_number2)
        self.assertTrue(status.is_success(dispatch1.status_code))
        self.assertTrue(status.is_success(dispatch2.status_code))

        response = self.client.get(reverse('flight_list'))
        self.assertTrue(status.is_success(response.status_code))
        self.assertContains(response, text=flt_number1, count=1)
        self.assertContains(response, text=flt_number2, count=1)

    def test_get_flight(self):
        flt_number = "NR003"

        self.authenticate()
        dispatch = self.dispatch(flt_number=flt_number)
        self.assertTrue(status.is_success(dispatch.status_code))

        response = self.client.get(reverse('flight', args=[flt_number]))
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['flt_number'], flt_number)

    def test_put_flight(self):
        flt_number1 = "NR004"
        flt_number2 = "NR005"

        self.authenticate()
        dispatch1 = self.dispatch(flt_number=flt_number1)
        dispatch2 = self.dispatch(flt_number=flt_number2)
        self.assertTrue(status.is_success(dispatch1.status_code))
        self.assertTrue(status.is_success(dispatch2.status_code))

        response1 = self.client.put(
            path=reverse('flight', args=[flt_number1]),
            content_type='application/json',
            data={"flt_number": "NR005"}
        )
        self.assertTrue(status.is_client_error(response1.status_code))
        self.assertTrue("flt_number" in response1.data)

        departure = create_airport("Departure airport")
        arrival = create_airport("Arrival airport")
        response2 = self.client.put(
            path=reverse('flight', args=[flt_number2]),
            content_type='application/json',
            data={
                "flt_number": "NR006",
                "acf_type": "A320",
                "departure_time": timezone.now() + timezone.timedelta(hours=2),
                "departure_airport": departure.icao_code,
                "arrival_airport": arrival.icao_code,
            }
        )
        self.assertTrue(status.is_success(response2.status_code))

    def test_delete_flight(self):
        flt_number = "NR007"

        self.authenticate()
        dispatch = self.dispatch(flt_number=flt_number)
        self.assertTrue(status.is_success(dispatch.status_code))

        response1 = self.client.delete(reverse('flight', args=["NR999"]))
        response2 = self.client.delete(reverse('flight', args=[flt_number]))
        self.assertTrue(status.is_client_error(response1.status_code))
        self.assertTrue(status.is_success(response2.status_code))


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
