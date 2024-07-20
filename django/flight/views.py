from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from pilot.permissions import IsPilot
from .models import Flight
from .serializers import FlightSerializer


@api_view(['POST'])
@permission_classes([IsPilot])
def dispatch(request):
    flight = FlightSerializer(
        data=request.data,
        context={'request': request}
    )
    flight.is_valid(raise_exception=True)
    flight.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsPilot])
def flight_list(request):
    serializer = FlightSerializer(Flight.objects.all(), many=True)
    return Response(serializer.data)


class FlightDetail(APIView):
    permission_classes = [IsPilot]

    def get_object(self, flt_number):
        return get_object_or_404(Flight, flt_number=flt_number)

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
