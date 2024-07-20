from django.db import models

from member.models import Member


class Pilot(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    simbrief_id = models.CharField(max_length=32)
    acars_api = models.CharField(max_length=255, unique=True)
    greetings = models.CharField(max_length=128)
    livestream_url = models.CharField(max_length=255)
