from rest_framework import viewsets, permissions

from .models import Member
from .serializers import MemberSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-last_login')
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
