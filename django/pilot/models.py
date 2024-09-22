from django.db import models
from django.utils.translation import gettext_lazy as _

from member.models import Member


class Pilot(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    simbrief_id = models.CharField(max_length=32)
    acars_api = models.CharField(max_length=255)
    greetings = models.CharField(max_length=128)
    livestream_url = models.CharField(max_length=255)


class PilotStats(models.Model):
    class Rank(models.TextChoices):
        CADET = "CAD", _("Cadet"),
        SECOND_OFFICER = "SEO", _("Second Officer"),
        FIRST_OFFICER = "FIO", _("First Officer"),
        CAPTAIN = "CPT", _("Captain"),
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    flight_count = models.IntegerField(default=0)
    flight_hours = models.IntegerField(default=0)
    rank = models.CharField(max_length=3, choices=Rank, default=Rank.CADET)
    experience = models.IntegerField(default=0)
