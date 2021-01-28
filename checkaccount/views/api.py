from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from checkaccount.models.models import CheckAccount, SysPersonnel, Sectors, Cities, Districts
from checkaccount.models.serializers import CheckAccountSerializer
from checkaccount.models.serializers import SysPersonnelSerializer, SectorsSerializer, CitySerializer, \
    DistrictSerializer
from checkaccount.views.permissions import CheckAccountPermission


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = CheckAccount.objects.all().order_by('-created_date')
    serializer_class = CheckAccountSerializer

    permission_classes = [
        IsAuthenticated,
        CheckAccountPermission
    ]

    def get_queryset(self):
        return super(CheckAccountAPI, self).get_queryset()

    def create(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).create(request, *args, **kwargs)


class SysPersonnelAPI(viewsets.ModelViewSet):
    queryset = SysPersonnel.objects.all().order_by('-created_date')
    serializer_class = SysPersonnelSerializer
    permission_classes = [
        # IsAuthenticated
    ]


class SectorsAPI(viewsets.ModelViewSet):
    queryset = Sectors.objects.all().order_by('-created_date')
    serializer_class = SectorsSerializer
    permission_classes = [
        # IsAuthenticated
    ]


class CitiesAPI(viewsets.ModelViewSet):
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [
        # IsAuthenticatedOrReadOnly
    ]


class DistrictAPI(viewsets.ModelViewSet):
    queryset = Districts.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [
        # IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        city_name = str(self.request.query_params.get('city')).upper()
        city = Cities.objects.get(name__contains=city_name)
        district_list = Districts.objects.filter(city=city)
        return district_list
