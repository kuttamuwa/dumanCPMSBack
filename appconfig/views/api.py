from avatar.models import Avatar
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from appconfig.models.models import Domains, Subtypes
from appconfig.models.serializers import DomainSerializer, SubtypeSerializer, AvatarSerializer
from appconfig.views.permissions import DomainPermission, SubtypePermission


class DomainsAPI(viewsets.ModelViewSet):
    queryset = Domains.objects.all().order_by('-created_date')
    serializer_class = DomainSerializer

    permission_classes = [IsAuthenticated, DomainPermission]


class SubtypesAPI(viewsets.ModelViewSet):
    queryset = Subtypes.objects.all().order_by('-created_date')
    serializer_class = SubtypeSerializer
    permission_classes = [IsAuthenticated, SubtypePermission]


class AvatarAPI(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):

       return super(AvatarAPI, self).get_queryset()
