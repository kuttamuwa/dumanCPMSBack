from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appconfig.models.models import Domains
from riskanalysis.controller.util import RiskAnalysisUtil
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.models.serializers import RiskPointsSerializer, DatasetSerializer, RiskPointsGetSerializer, \
    RiskPointsPostSerializer
from riskanalysis.views.permissions import DatasetPermission, RiskPointsPermission


class DatasetAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = DatasetSerializer

    permission_classes = [
        # IsAuthenticated, DatasetPermission
    ]

    @staticmethod
    def fill_all_points(again=False):
        RiskPointsAPI().analyze_all(again)

    def get_queryset(self):
        self.fill_all_points()
        qset = super(DatasetAPI, self).get_queryset()

        return qset


class RiskPointsAPI(viewsets.ModelViewSet):
    queryset = RiskDataSetPoints.objects.all().order_by('-created_date')
    serializer_class = RiskPointsSerializer  # general serializer
    permission_classes = [
        # IsAuthenticated, RiskPointsPermission
    ]

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
        qset = qset.filter(risk_dataset__in=rd)
        return qset

    def analyze_all(self, again=False):
        for rd in DataSetModel.objects.all():
            self.analyze_data(rd.pk, again=again)

    def analyze_data(self, riskdataset_pk, **kwargs):
        dataset = kwargs.get('riskdataset')
        again = kwargs.get('again')

        if dataset is None:
            if riskdataset_pk:
                dataset = self.get_one_riskdataset(pk=riskdataset_pk)
            else:
                RiskParamValueError(detail='Not enough data ! \n'
                                           'No primary key or dataset object was defined.')

        if dataset.general_point is None and again is False:
            rp = RiskDataSetPoints(risk_dataset=dataset, variable='TOPLAM')
            analyzer = rp.analyzer(rp.risk_dataset)
            try:
                general_point = analyzer.analyze()
                rp.point = general_point
                dataset.general_point = general_point

                dataset.save()
                rp.save()
            except Domains.DoesNotExist:
                return DomainDoesNotExist

            except ValueError as err:
                return RiskParamValueError(detail=err)

            return rp

    def create(self, request, *args, **kwargs):
        """
        Creation işlemi risk points hesaplamalarında izin verilmez. Buraya gelen create isteği aslında
        risk_dataset parametresi verilmiş
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            pk = int(request.POST['risk_dataset'])
            rp = self.analyze_data(riskdataset_pk=pk)
            rp.save()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

        except ValueError:
            return RiskParamValueError

        except KeyError:
            return RiskParamValueError(detail='Muhtemelen risk analiz parametresi vermediniz. \n'
                                              'APIye risk_dataset=1 gibi göndermelisiniz')

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
