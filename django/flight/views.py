from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from pilot.permissions import IsPilot
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
    return Response(data="Dispatch success.", status=status.HTTP_201_CREATED)
