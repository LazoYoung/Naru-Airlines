from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from pilot.models import Pilot, PilotStats
from pilot.permissions import IsPilot


@api_view(['GET'])
@permission_classes([IsPilot])
def stats(request: Request):
    pilot = Pilot.objects.filter(member=request.user)
    model = PilotStats.objects.filter(pilot=pilot)

    if model.exists():
        stat = model.get()
    else:
        stat = PilotStats.objects.create(pilot=pilot)

    data = {
        'flight_count': stat.flight_count,
        'flight_hour': stat.flight_hour,
        'rank': PilotStats.Rank[stat.rank].label,
        'experience': stat.experience,
        'grade': (
                PilotStats
                .objects
                .filter(experience__gte=stat.experience)
                .count() + 1
        )
    }

    return Response(data=data, status=status.HTTP_200_OK)
