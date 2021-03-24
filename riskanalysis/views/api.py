import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from appconfig.models.models import Domains
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.models.serializers import RiskPointsSerializer, RiskPointsGetSerializer, \
    DatasetSerializerLimited, DatasetSerializerGeneral
from riskanalysis.views.permissions import DatasetPermission, RiskPointsPermission


class DatasetRenderer(JSONRenderer):
    pass


class DatasetAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = DatasetSerializerGeneral
    # renderer_classes = [DatasetRenderer]

    permission_classes = [
        IsAuthenticated,
        DatasetPermission
    ]

    @staticmethod
    def fill_all_points(again=False):
        RiskPointsAPI().analyze_all(again)

    def get_queryset(self):
        self.fill_all_points()
        qset = super(DatasetAPI, self).get_queryset()
        return qset

    def retrieve(self, request, *args, **kwargs):
        ret = super(DatasetAPI, self).retrieve(request, *args, **kwargs)
        return ret

    @staticmethod
    def handle_excel_file(file, errors, state):
        try:
            if file.name.endswith('.xlsx'):
                save_path = os.path.join(settings.MEDIA_ROOT, 'rduploads', str(uuid.uuid1()) + ".xlsx")
                save_path = default_storage.save(save_path, file)

                # Trigger the risk dataset
                try:
                    DataSetModel().read_from_excel(save_path)
                except Exception as err:
                    # herhangi bi hata cikmis olabilir
                    errors.append(err)
                    state = status.HTTP_417_EXPECTATION_FAILED
                finally:
                    os.remove(save_path)

        except KeyError:
            errors.append("Risk analiz verisini ancak excel ile yükleyebilirsiniz ! \n"
                          "API keyword: excel_file")
            state = status.HTTP_400_BAD_REQUEST

        return errors, state

    def create(self, request, *args, **kwargs):
        # file uploading or filling manually
        errors = []
        state = status.HTTP_200_OK
        excel_file = request.FILES['excel']
        errors, state = self.handle_excel_file(excel_file, errors, state)

        return Response(data={
            'errors': errors,
        }, status=state
        )

    def update(self, request, *args, **kwargs):
        return super(DatasetAPI, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(DatasetAPI, self).destroy(request, *args, **kwargs)


class RiskPointsAPI(viewsets.ModelViewSet):
    queryset = RiskDataSetPoints.objects.all().order_by('-created_date')
    serializer_class = RiskPointsSerializer  # general serializer
    permission_classes = [
        IsAuthenticated,
        RiskPointsPermission
    ]
    http_method_names = ['get', 'head']

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
        if len(DataSetModel.objects.all()) != 0:
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

        if isinstance(dataset, DataSetModel):
            if dataset.general_point is None or again:
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

                return general_point
            else:
                return dataset.general_point

        else:
            return {
                "error": dataset
            }

    def create(self, request, *args, **kwargs):
        """
        Creation işlemi risk points hesaplamalarında izin verilmez. Buraya gelen create isteği aslında POST
        risk_dataset parametresi verilmiş
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            pk = int(request.query_params['riskdataset_pk'])
            again = bool(request.query_params.get('again', False))  # söylenmezse yapılmaz

            resp = self.analyze_data(riskdataset_pk=pk, again=again)

            if isinstance(resp, float):
                return Response(resp, status=status.HTTP_200_OK)
            else:
                err = resp['error']
                return Response(err.default_detail,
                                status=err.status_code,
                                exception=True)
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
