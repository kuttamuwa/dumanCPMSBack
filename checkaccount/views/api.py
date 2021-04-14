from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from checkaccount.models.models import CheckAccount, SysPersonnel, Sectors, Cities, Districts
from checkaccount.models.serializers import CheckAccountSerializer
from checkaccount.models.serializers import SysPersonnelSerializer, SectorsSerializer, CitySerializer, \
    DistrictSerializer
from checkaccount.views.permissions import CheckAccountPermission
from riskanalysis.models.models import DataSetModel


class CheckAccountPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = CheckAccount.objects.all().order_by('-created_date')
    pagination_class = CheckAccountPagination
    serializer_class = CheckAccountSerializer
    permission_classes = [
        IsAuthenticated,
        CheckAccountPermission
    ]

    http_method_names = ['get', 'post', 'head', 'put', 'update', 'patch', 'delete']

    def retrieve(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).retrieve(request, *args, **kwargs)

    def param_parser(self):
        qparams = self.request.query_params
        qparams = {k: v for k, v in qparams.items() if k not in ('encoding',)}

        # dummy parameter
        dummy = qparams.get('dummy', True)
        if dummy == 'false':
            dummy = False
        elif dummy == 'true':
            dummy = True
        qparams['dummy'] = dummy

        return qparams

    def list(self, request, *args, **kwargs):
        qparams = self.param_parser()
        self.queryset = self.queryset.filter(**qparams)

        return super(CheckAccountAPI, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).create(request, *args, **kwargs)


class SysPersonnelAPI(viewsets.ModelViewSet):
    queryset = SysPersonnel.objects.all().order_by('-created_date')
    serializer_class = SysPersonnelSerializer
    permission_classes = [
        IsAuthenticated
    ]


class SectorsAPI(viewsets.ModelViewSet):
    queryset = Sectors.objects.all().order_by('-created_date')
    serializer_class = SectorsSerializer
    permission_classes = [
        IsAuthenticated
    ]


class CitiesAPI(viewsets.ModelViewSet):
    queryset = Cities.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]


class DistrictAPI(viewsets.ModelViewSet):
    queryset = Districts.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        if self.request.query_params:
            city_name = str(self.request.query_params.get('city')).upper()
            city = Cities.objects.get(name__contains=city_name)
            district_list = Districts.objects.filter(city=city)

        else:
            district_list = Districts.objects.all()

        return district_list
