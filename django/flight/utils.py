import random
import string

from django.http import QueryDict
from django.urls.base import reverse
from django.utils.http import urlencode
from rest_framework.request import Request

from flight.models import Airport, Aircraft


def get_dummy_aircraft():
    return Aircraft.objects.get_or_create(
        icao_code="A320",
        defaults={
            "registration": "HL1234",
            "name": "Airbus A320 IAE",
        }
    )[0]


def create_airport(icao_code=None):
    return Airport.objects.create(
        name=_random_string(),
        icao_code=icao_code if icao_code else _random_airport_code(True),
        iata_code=_random_airport_code(False),
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


def _random_string(length=6):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def _random_airport_code(icao=True):
    length = 4 if icao else 3
    field = 'icao_code' if icao else 'iata_code'
    while True:
        seq = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(seq) for _ in range(length))
        if code not in Airport.objects.values_list(field, flat=True):
            return code


def has_query(request: Request):
    return len(request.query_params.keys()) > 0


def reverse_query(view, urlconf=None, args=None, kwargs=None, current_app=None, query=None):
    base_url = reverse(viewname=view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)

    if query is None:
        return base_url

    if isinstance(query, str):
        query = {query: ''}
    elif isinstance(query, list) or isinstance(query, tuple):
        query = {(e, '') for e in query}

    return "{}?{}".format(base_url, urlencode(query))
