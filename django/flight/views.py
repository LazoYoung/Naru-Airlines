from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pilot.permissions import IsPilotOrReadOnly
from .serializers import FlightSerializer
from .models import Flight


@api_view(['POST'])
@permission_classes([IsPilotOrReadOnly])
def dispatch(request):
    flight = FlightSerializer(
        data=request.data,
        context={'request': request}
    )
    flight.is_valid(raise_exception=True)
    flight.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsPilotOrReadOnly])
def schedules(request: Request):
    queryset = (
        Flight
        .objects
        .filter(pilot=request.user.pilot)
        .order_by('departure_time')
    )
    serializer = FlightSerializer(queryset, many=True)
    return Response(serializer.data)


class ScheduleAPI(APIView):
    permission_classes = [IsPilotOrReadOnly]

    def get_object(self, flt_number):
        obj = get_object_or_404(Flight, flt_number=flt_number)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, flt_number):
        serializer = FlightSerializer(instance=self.get_object(flt_number))
        return Response(serializer.data)

    def put(self, request, flt_number):
        serializer = FlightSerializer(
            instance=self.get_object(flt_number),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, flt_number):
        self.get_object(flt_number).delete()
        return Response(status=status.HTTP_200_OK)
