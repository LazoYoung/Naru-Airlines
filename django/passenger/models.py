from django.db import models

from member.models import Member


class Passenger(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    mileage = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.member.email

    @staticmethod
    def get(member):
        pax, created = Passenger.objects.get_or_create(member=member)
        return pax


class Booking(models.Model):
    ticket_number = models.PositiveBigIntegerField(primary_key=True)
    member = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    # todo: fk to a dispatched flight
