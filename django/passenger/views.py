from rest_framework.decorators import api_view
from rest_framework.response import Response

from flight.models import Flight
from flight.serializers import FlightSerializer


@api_view(['GET'])
def timetable(request):
    queryset = (
        Flight
        .objects
        .filter(phase=Flight.Phase.SCHEDULED)
        .order_by('departure_time')
    )
    serializer = FlightSerializer(queryset, many=True)
    return Response(serializer.data)
