from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from checkaccount.models.models import CheckAccount, SysPersonnel, Sectors, Cities, Districts
from checkaccount.models.serializers import CheckAccountSerializer
from checkaccount.models.serializers import SysPersonnelSerializer, SectorsSerializer, CitySerializer, \
    DistrictSerializer
from checkaccount.views.permissions import CheckAccountPermission
from riskanalysis.models.models import DataSetModel


class CheckAccountAPI(viewsets.ModelViewSet):
    queryset = CheckAccount.objects.all().order_by('-created_date')
    serializer_class = CheckAccountSerializer
    permission_classes = [
        IsAuthenticated,
        CheckAccountPermission
    ]
    # lookup_field = 'pk'
    http_method_names = ['get', 'post', 'head', 'put', 'update', 'patch', 'delete']

    def get_queryset(self):
        qset = super(CheckAccountAPI, self).get_queryset()
        pk = self.request.query_params.get('pk')
        if pk:
            qset = qset.filter(pk=pk)

        return qset

    def create(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).retrieve(request, *args, **kwargs)

    @staticmethod
    def fill_some_fields_auto(request):
        request.POST._mutable = True

        request.POST['web_url'] = 'https://cli.vuejs.org/guide/mode-and-env.html#environment-variables'
        request.POST['email_addr'] = 'ucok.umut@gmail.com'

        request.POST._mutable = False
        return request

    def update(self, request, *args, **kwargs):
        return super(CheckAccountAPI, self).update(request, *args, **kwargs)


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
        city_name = str(self.request.query_params.get('city')).upper()
        city = Cities.objects.get(name__contains=city_name)
        district_list = Districts.objects.filter(city=city)
        return district_list
