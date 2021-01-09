from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from checkaccount.models.models import CheckAccount, AccountDocuments, PartnershipDocuments, SysPersonnel, Sectors, \
    Cities, \
    Districts
from checkaccount.models.serializers import CheckAccountSerializer, AccountDocumentsSerializer, \
    PartnershipDocumentsSerializer
from checkaccount.models.serializers import SysPersonnelSerializer, SectorsSerializer, CitySerializer, \
    DistrictSerializer
from checkaccount.views.permissions import CheckAccountPermission


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = CheckAccount.objects.all().order_by('-created_date')
    serializer_class = CheckAccountSerializer

    permission_classes = [IsAuthenticated, CheckAccountPermission]


class AccountDocumentsAPI(viewsets.ModelViewSet):
    queryset = AccountDocuments.objects.all().order_by('-created_date')
    serializer_class = AccountDocumentsSerializer
    permission_classes = [IsAuthenticated, CheckAccountPermission]


class PartnershipDocumentsAPI(viewsets.ModelViewSet):
    queryset = PartnershipDocuments.objects.all().order_by('-created_date')
    serializer_class = PartnershipDocumentsSerializer
    permission_classes = [IsAuthenticated, CheckAccountPermission]


class SysPersonnelAPI(viewsets.ModelViewSet):
    queryset = SysPersonnel.objects.all().order_by('-created_date')
    serializer_class = SysPersonnelSerializer
    permission_classes = [IsAuthenticated]


class SectorsAPI(viewsets.ModelViewSet):
    queryset = Sectors.objects.all().order_by('-created_date')
    serializer_class = SectorsSerializer
    permission_classes = [IsAuthenticated]


class CitiesAPI(viewsets.ModelViewSet):
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DistrictAPI(viewsets.ModelViewSet):
    queryset = Districts.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        city_pk = self.request.query_params.get('city_pk')
        city = Cities.objects.filter(pk=city_pk)

        return city
