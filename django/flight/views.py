from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from member.permission import IsAdminOrReadOnly
from pilot.permissions import IsPilotOrReadOnly
from .models import FlightSchedule, Aircraft, StandardRoute
from .serializers import AircraftSerializer, StandardRouteSerializer, DispatchStandardSerializer, \
    DispatchCharterSerializer, FlightScheduleSerializer
from .services import DispatcherService, StandardDTO, CharterDTO, DispatchError


@api_view(['GET'])
def routes(request):
    data = StandardRoute.objects.all().values()
    return Response(data=data, status=status.HTTP_200_OK)


class RouteAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, flight_number):
        serializer = StandardRouteSerializer(instance=self._route(flight_number))
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = StandardRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, flight_number):
        serializer = StandardRouteSerializer(
            instance=self._route(flight_number),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, flight_number):
        instance = self._route(flight_number)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _route(flight_number):
        return get_object_or_404(StandardRoute, flight_number=flight_number)


@api_view(['GET'])
def fleet_profiles(request):
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
def dispatch_standard(request: Request):
    serializer = DispatchStandardSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    dto = StandardDTO(
        flight_number=data['flight_number'],
        aircraft=data.get('aircraft'),
    )

    service = DispatcherService(request.user.pilot)
    try:
        schedule = service.dispatch_standard(dto)
        serializer = FlightScheduleSerializer(instance=schedule)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except DispatchError as e:
        return e.response()


@api_view(['POST'])
@permission_classes([IsPilotOrReadOnly])
def dispatch_charter(request: Request):
    serializer = DispatchCharterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    dto = CharterDTO(
        aircraft=data['aircraft'],
        flight_time=data['flight_time'],
        departure_time=data['departure_time'],
        departure_airport=data['departure_airport'],
        arrival_airport=data['arrival_airport'],
    )

    service = DispatcherService(request.user.pilot)
    try:
        schedule = service.dispatch_charter(dto)
        serializer = FlightScheduleSerializer(instance=schedule)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except DispatchError as e:
        return e.response()


@api_view(['GET'])
@permission_classes([IsPilotOrReadOnly])
def schedules_all(request: Request):
    queryset = (
        FlightSchedule
        .objects
        .order_by('departure_time')
    )
    serializer = FlightScheduleSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsPilotOrReadOnly])
def schedules_mine(request: Request):
    queryset = (
        FlightSchedule
        .objects
        .filter(pilot=request.user.pilot)
        .order_by('departure_time')
    )
    serializer = FlightScheduleSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsPilotOrReadOnly])
def schedules_available(request: Request):
    queryset = (
        FlightSchedule
        .objects
        .filter(pilot__isnull=True)
        .order_by('departure_time')
    )
    serializer = FlightScheduleSerializer(queryset, many=True)
    return Response(serializer.data)


class ScheduleAPI(APIView):
    permission_classes = [IsPilotOrReadOnly]

    def get_object(self, flight_number):
        obj = get_object_or_404(FlightSchedule, flight_number=flight_number)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, flight_number):
        serializer = FlightScheduleSerializer(instance=self.get_object(flight_number))
        return Response(serializer.data)

    # def put(self, request, flight_number):
    #     serializer = FlightScheduleSerializer(
    #         instance=self.get_object(flight_number),
    #         data=request.data,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, flight_number):
        schedule = self.get_object(flight_number)
        self.check_object_permissions(self.request, schedule)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
