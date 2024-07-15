from django.contrib.auth import get_user_model
from django.db import models


class Passenger(models.Model):
    member = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    mileage = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.member.primary_key

    @staticmethod
    def get(member):
        pax, created = Passenger.objects.get_or_create(member=member)
        return pax
