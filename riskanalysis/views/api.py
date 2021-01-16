from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from appconfig.models.models import Domains
from riskanalysis.controller.util import RiskAnalysisUtil
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.models.serializers import RiskPointsSerializer, DatasetSerializer, RiskPointsGetSerializer, \
    RiskPointsPostSerializer
from riskanalysis.views.permissions import DatasetPermission, RiskPointsPermission


class DatasetAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = DatasetSerializer

    permission_classes = [IsAuthenticated, DatasetPermission]

    def get_queryset(self):
        self.import_data()
        return super(DatasetAPI, self).get_queryset()

    @staticmethod
    def import_data(load_again=True):
        if load_again:
            DataSetModel.objects.all().delete()

        mpys = r"C:\Users\LENOVO\PycharmProjects\dumanCPMSRevise\riskanalysis\data\OrnekMPYSTurkcev2.xlsx"
        util = RiskAnalysisUtil()
        data_list = util.import_from_excel(mpys)
        for i in data_list:
            rd = DataSetModel.objects.get_or_create(**i)
            rd.save()


class RiskPointsAPI(viewsets.ModelViewSet):
    queryset = RiskDataSetPoints.objects.all().order_by('-created_date')
    serializer_class = RiskPointsSerializer  # general serializer
    permission_classes = [IsAuthenticated, RiskPointsPermission]

    # lookup_field = 'data_id'

    @staticmethod
    def test_create_point():
        rd = DataSetModel.objects.first()
        pnt = RiskDataSetPoints(risk_dataset=rd, variable='TOPLAM', point=47.4)
        pnt.save()

    def __get_riskdataset(self):
        return DataSetModel.objects.filter(**self.kwargs)

    @staticmethod
    def get_one_riskdataset(*args, **kwargs):
        try:
            return DataSetModel.objects.get(*args, **kwargs)

        except DataSetModel.MultipleObjectsReturned:
            return ManyRiskDataset

        except DataSetModel.DoesNotExist:
            return NoRiskDataset

    def get_method_queryset(self, qset):
        self.serializer_class = RiskPointsGetSerializer
        rd = self.__get_riskdataset()
        qset = qset.filter(variable='TOPLAM', risk_dataset__in=rd)
        return qset

    def post_method_queryset(self, qset):
        self.serializer_class = RiskPointsPostSerializer
        return qset

    def analyze_data(self, riskdataset_pk):
        if riskdataset_pk:
            rd = self.get_one_riskdataset(pk=riskdataset_pk)
            rp = RiskDataSetPoints(risk_dataset=rd, variable='TOPLAM')
            analyzer = rp.analyzer(rp.risk_dataset)
            try:
                general_pts = analyzer.analyze()
                rp.point = general_pts
            except Domains.DoesNotExist:
                return DomainDoesNotExist

            except ValueError as err:
                r = RiskParamValueError(detail=err)
                return r

    def create(self, request, *args, **kwargs):
        try:
            pk = int(request.POST.get('risk_dataset'))
            self.analyze_data(riskdataset_pk=pk)
            return self.retrieve(request, *args, **kwargs)
        except ValueError:
            return RiskParamValueError

    def get_queryset(self):
        qset = super(RiskPointsAPI, self).get_queryset()

        # if self.request.method == 'GET':
        qset = self.get_method_queryset(qset)

        return qset


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service geçici olarak kullanıma kapalıdır, lütfen tekrar deneyiniz.'
    default_code = 'service_unavailable'


class ManyRiskDataset(APIException):
    status_code = 404
    default_detail = 'Analiz yaptırmak için tek tek seçmeniz gerekir. Tüm objelere analiz yapılamaz.'
    default_code = 'NotImplementedError'


class NoRiskDataset(APIException):
    status_code = 404
    default_detail = 'Analiz için gerekli veri seti bulunamadı !'
    default_code = 'DoesNotExists'


class RiskParamValueError(APIException):
    status_code = 404
    default_detail = 'Muhtemelen risk analizi için verdiğiniz değer sayı değil.'
    default_code = 'ValueError'


class DomainDoesNotExist(APIException):
    status_code = 404
    default_detail = 'Domain verilerinizde hata vardır. Lütfen verileri yüklediğinizden ve subtype ' \
                     'içerisindeki domain_name kısmındaki domainlerin Domains.xlsx dosyasında da olduğundan ' \
                     'emin olunuz'
