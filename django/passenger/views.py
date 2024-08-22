from rest_framework.decorators import api_view
from rest_framework.response import Response

from flight.models import FlightSchedule
from flight.serializers import FlightScheduleSerializer


@api_view(['GET'])
def timetable(request):
    queryset = (
        FlightSchedule
        .objects
        .order_by('departure_time')
    )
    serializer = FlightScheduleSerializer(queryset, many=True)
    return Response(serializer.data)
