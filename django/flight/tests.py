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

    def test_bad_airport(self):
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
