from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics, viewsets, parsers
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)



class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UpdateUser(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def get_object(self):
        return User.objects.get(uuid=self.request.user.uuid)

class GetStaff(generics.ListAPIView):
    serializer_class = UserStaffSerializer
    def get_queryset(self):
        return User.objects.filter(
    Q(is_teacher=True) | Q(is_staff=True) | Q(is_manager=True),
    is_superuser=False
)
class GetStaffBySlug(generics.RetrieveAPIView):
    serializer_class = UserStaffSerializer
    queryset = User.objects.all()
    lookup_field = 'slug'
