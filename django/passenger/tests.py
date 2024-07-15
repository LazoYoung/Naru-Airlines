from django.contrib.auth import get_user_model
from django.test import TestCase

from member.utils import get_random_password, get_random_email, get_random_string
from .models import Passenger


class TestPassengerRelation(TestCase):
    def test_create_passenger(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            handle=get_random_string(8), display_name=get_random_string(8),
            email=get_random_email(), password=get_random_password()
        )

        # pax: Passenger = user.passenger
        pax = Passenger.get(user)

        self.assertTrue(hasattr(user, 'passenger'))
        self.assertTrue(isinstance(pax, Passenger))
        self.assertEqual(pax.mileage, 0)
