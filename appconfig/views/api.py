from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from appconfig.models.models import Domains, Subtypes
from appconfig.models.serializers import DomainSerializer, SubtypeSerializer
from appconfig.views.permissions import DomainPermission, SubtypePermission


class DomainsAPI(viewsets.ModelViewSet):
    queryset = Domains.objects.all().order_by('-created_date')
    serializer_class = DomainSerializer

    permission_classes = [IsAuthenticated, DomainPermission]


class SubtypesAPI(viewsets.ModelViewSet):
    queryset = Subtypes.objects.all().order_by('-created_date')
    serializer_class = SubtypeSerializer
    permission_classes = [IsAuthenticated, SubtypePermission]

