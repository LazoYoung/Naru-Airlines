from datetime import datetime, date

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from member.permission import IsAdminOrReadOnly
from pilot.permissions import IsPilot
from .models import FlightSchedule, Aircraft, StandardRoute
from .serializers import AircraftSerializer, StandardRouteSerializer, DispatchRoutineSerializer, \
    DispatchCharterSerializer, FlightScheduleSerializer
from .services import DispatcherService, RoutineDTO, CharterDTO, DispatchError
from .utils import has_query


class RoutesAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    @staticmethod
    def get(request: Request):
        qs = StandardRoute.objects.all()
        dep = request.query_params.get("departure_airport")
        arr = request.query_params.get("arrival_airport")
        aircraft = request.query_params.get("aircraft")

        if dep:
            qs = qs.filter(departure_airport=dep)

        if arr:
            qs = qs.filter(arrival_airport=arr)

        if aircraft:
            qs = qs.filter(aircraft=aircraft)

        serializer = StandardRouteSerializer(instance=qs, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = StandardRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RouteAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, flight_number):
        serializer = StandardRouteSerializer(instance=self._route(flight_number))
        return Response(serializer.data)

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


class FleetAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def get(request: Request):
        queryset = Aircraft.objects.all()
        serializer = AircraftSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request: Request):
        serializer = AircraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AircraftAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, icao_code):
        serializer = AircraftSerializer(instance=self._instance(icao_code))
        return Response(serializer.data)

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
@permission_classes([IsPilot])
def dispatch_routine(request: Request):
    serializer = DispatchRoutineSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    dto = RoutineDTO(
        flight_number=data['flight_number'],
        aircraft=data.get('aircraft'),
    )

    service = DispatcherService(request.user.pilot)
    try:
        schedule = service.dispatch_routine(dto)
        serializer = FlightScheduleSerializer(instance=schedule)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except DispatchError as e:
        return e.response()


@api_view(['POST'])
@permission_classes([IsPilot])
def dispatch_charter(request: Request):
    serializer = DispatchCharterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    dto = CharterDTO(
        aircraft=data['aircraft'],
        block_time=data['block_time'],
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


class SchedulesAPI(APIView):
    permission_classes = (IsPilot,)

    def get(self, request: Request):
        if 'mine' in request.query_params:
            qs = self._my_schedules(request)
        elif 'available' in request.query_params:
            qs = self._available_schedules(request)
        else:
            qs = self._all_schedules(request)

        dep = request.query_params.get("departure_airport")
        arr = request.query_params.get("arrival_airport")
        aircraft = request.query_params.get("aircraft")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if dep:
            qs = qs.filter(departure_airport=dep)

        if arr:
            qs = qs.filter(arrival_airport=arr)

        if aircraft:
            qs = qs.filter(aircraft=aircraft)

        if date_from and date_to:
            try:
                date_from = date.fromisoformat(date_from)
                date_to = date.fromisoformat(date_to)
                qs = qs.filter(departure_time__date__range=(date_from, date_to))
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)

        qs = qs.order_by('departure_time')

        serializer = FlightScheduleSerializer(instance=qs, many=True)
        return Response(serializer.data)

    @staticmethod
    def _all_schedules(request: Request):
        return FlightSchedule.objects

    @staticmethod
    def _my_schedules(request: Request):
        return FlightSchedule.objects.filter(pilot=request.user.pilot)

    @staticmethod
    def _available_schedules(request: Request):
        return FlightSchedule.objects.filter(pilot__isnull=True)


class ScheduleAPI(APIView):
    permission_classes = (IsPilot,)

    def get(self, request, flight_number):
        serializer = FlightScheduleSerializer(instance=self._get_object(flight_number))
        return Response(serializer.data)

    def delete(self, request, flight_number):
        schedule = self._get_object(flight_number)
        self.check_object_permissions(self.request, schedule)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_object(self, flight_number):
        obj = get_object_or_404(FlightSchedule, flight_number=flight_number)
        self.check_object_permissions(self.request, obj)
        return obj
