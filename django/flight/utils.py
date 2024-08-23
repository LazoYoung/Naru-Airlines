import random
import string

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
