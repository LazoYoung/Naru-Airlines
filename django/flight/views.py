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
from .utils import has_query


class RouteAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request: Request):
        if has_query(request):
            if 'id' in request.query_params:
                flight_number = request.query_params.get('id')
                serializer = StandardRouteSerializer(instance=self._route(flight_number))
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = StandardRoute.objects.all()
            serializer = StandardRouteSerializer(instance=queryset, many=True)
            return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = StandardRouteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request: Request):
        if has_query(request):
            flight_number = request.query_params.get('id')
            serializer = StandardRouteSerializer(
                instance=self._route(flight_number),
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        if has_query(request):
            flight_number = request.query_params.get('id')
            instance = self._route(flight_number)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _route(flight_number):
        return get_object_or_404(StandardRoute, flight_number=flight_number)


@api_view(['GET'])
def fleet_profiles(request):
    return Response(data=Aircraft.objects.all().values(), status=status.HTTP_200_OK)


class FleetAPI(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request):
        if has_query(request):
            if 'id' in request.query_params:
                icao_code = request.query_params.get('id')
                serializer = AircraftSerializer(instance=self._instance(icao_code))
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Aircraft.objects.all()
            serializer = AircraftSerializer(instance=queryset, many=True)
            return Response(serializer.data)

    @staticmethod
    def post(request: Request):
        serializer = AircraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request: Request):
        if has_query(request):
            if 'id' in request.query_params:
                icao_code = request.query_params.get('id')
                serializer = AircraftSerializer(
                    instance=self._instance(icao_code),
                    data=request.data,
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        if has_query(request):
            if 'id' in request.query_params:
                icao_code = request.query_params.get('id')
                instance = self._instance(icao_code)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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


class ScheduleAPI(APIView):
    permission_classes = (IsPilotOrReadOnly,)

    def get(self, request: Request):
        keys: set = request.query_params.keys()

        if len(keys) == 0:
            queryset = self._all_schedules(request)
        elif 'mine' in keys:
            queryset = self._my_schedules(request)
        elif 'available' in keys:
            queryset = self._available_schedules(request)
        elif 'id' in keys:
            return self._single_schedule(request)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = FlightScheduleSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def delete(self, request: Request):
        flight_number = request.query_params.get('id')
        schedule = self._get_object(flight_number)
        self.check_object_permissions(self.request, schedule)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _single_schedule(self, request: Request):
        flight_number = request.query_params.get('id')
        serializer = FlightScheduleSerializer(instance=self._get_object(flight_number))
        return Response(serializer.data)

    def _get_object(self, flight_number):
        obj = get_object_or_404(FlightSchedule, flight_number=flight_number)
        self.check_object_permissions(self.request, obj)
        return obj

    def _my_schedules(self, request: Request):
        return self._queryset().filter(pilot=request.user.pilot).order_by('departure_time')

    def _all_schedules(self, request: Request):
        return self._queryset().order_by('departure_time')

    def _available_schedules(self, request: Request):
        return self._queryset().filter(pilot__isnull=True).order_by('departure_time')

    @staticmethod
    def _queryset():
        return FlightSchedule.objects
