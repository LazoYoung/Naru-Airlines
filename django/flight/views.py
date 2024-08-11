from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from member.permission import IsAdminOrReadOnly
from pilot.permissions import IsPilotOrReadOnly
from .models import Flight, Aircraft
from .serializers import FlightSerializer, AircraftSerializer


# todo: complete views
@api_view(['GET'])
def standard_routes(request):
    pass


class ManageRouteAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


@api_view(['POST'])
@permission_classes([IsPilotOrReadOnly])
def dispatch_standard(request):
    pass


@api_view(['GET'])
def fleet_all(request):
    return Response(data=Aircraft.objects.all().values(), status=status.HTTP_200_OK)


class AircraftAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, icao_code):
        serializer = AircraftSerializer(instance=self._instance(icao_code))
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = AircraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, icao_code):
        serializer = AircraftSerializer(
            instance=self._instance(icao_code),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, icao_code):
        instance = self._instance(icao_code)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _instance(icao_code):
        return get_object_or_404(Aircraft, icao_code=icao_code)


@api_view(['POST'])
@permission_classes([IsPilotOrReadOnly])
def dispatch_charter(request):
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

    def get_object(self, flight_number):
        obj = get_object_or_404(Flight, flight_number=flight_number)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, flight_number):
        serializer = FlightSerializer(instance=self.get_object(flight_number))
        return Response(serializer.data)

    def put(self, request, flight_number):
        serializer = FlightSerializer(
            instance=self.get_object(flight_number),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, flight_number):
        self.get_object(flight_number).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
