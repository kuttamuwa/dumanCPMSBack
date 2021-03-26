import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from appconfig.models.models import Domains
from checkaccount.models.models import CheckAccount
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.models.serializers import RiskPointsSerializer, RiskPointsGetSerializer, \
    DatasetSerializerGeneral, DatasetSerializerExclusive, CardSerializer
from riskanalysis.views.permissions import DatasetPermission, RiskPointsPermission, CardsPermissions


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
        try:
            excel_file = request.FILES['excel']
            errors, state = self.handle_excel_file(excel_file, errors, state)

            return Response(data={
                'errors': errors,
            }, status=state
            )
        except KeyError:
            print("Excel gonderilmiyor, direkt kayit acilacak")
            return super(DatasetAPI, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(DatasetAPI, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(DatasetAPI, self).destroy(request, *args, **kwargs)


class DatasetExAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all()
    serializer_class = DatasetSerializerExclusive

    permission_classes = [
        IsAuthenticated,
        DatasetPermission
    ]

    def create(self, request, *args, **kwargs):
        rd = super(DatasetExAPI, self).create(request, *args, **kwargs)
        self._analyze_it(rd)

        return rd

    def _analyze_it(self, rd):
        """
        request to analyzer api
        :param rd:
        :return:
        """
        d_id = rd.data.get('data_id')
        rd = DataSetModel.objects.get(data_id=d_id)
        try:
            rp = RiskDataSetPoints(risk_dataset=rd, variable='TOPLAM')
            analyzer = rp.analyzer(rp.risk_dataset)
            general_point = analyzer.analyze(get_subpoints=False)
            rp.point = general_point
            rp.save()
            rd.general_point = general_point
            rd.save()

        except Exception as err:
            return Response(
                status=500,
                data=err
            )


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
                    general_point = analyzer.analyze(get_subpoints=False)
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


class CardsAPI(viewsets.ReadOnlyModelViewSet):
    """
    Kartlar için kullanılan API'dir.

    Sağlanan veriler:
        3 Tipte veri getirir:
        * Limit aşımları
        * ADH
        * Yeni Müşteri Raporu
        * Müşteri Performans Raporu
        * Vade Aşımı Raporu
        * Uyarılar

    * Kullanım
    pk verilirse tekil müşterinin, verilmezse 5 müşterinin kaydı getirilir. Daha fazla kayıt isteniyorsa
    count parametresi belirtilmeli.

        Limit aşımları: dtype=l -> Tekil de çoğul da kullanılabilir. Ör:
            ..:8000/riskanalysis/api/dashboard/12/?dtype=l
            ..:8000/riskanalysis/api/dashboard/?dtype=l

        Alacak Devir hızı: dtype=adh -> Tekil + Çoğul. Ör:

    """
    queryset = DataSetModel.objects.all()
    serializer_class = CardSerializer
    permission_classes = [
        IsAuthenticated,
        CardsPermissions
    ]

    def param_parser(self, dtype, multi=False, pk=None, **kwargs):
        if dtype == 'l':
            return self.limit_bakiye(dataset_id=pk, multi=multi, **kwargs)

        elif dtype == 'adh':
            return self.adh(dataset_id=pk, multi=multi, **kwargs)

        elif dtype == 'ym':
            return self.son_eklenen_musteriler(**kwargs)

    def list_checks(self, request, *args, **kwargs):
        pass

    def retrieve_checks(self):
        qparam = self.request.query_params
        pk = self.request.parser_context.get('kwargs').get('pk')
        dtype = qparam.get('dtype')

        return qparam, pk, dtype

    def _init_values(self):
        qparam, pk, dtype = self.retrieve_checks()
        other_params = {k: v for k, v in qparam.items() if k not in ('dtype', 'pk')}

        return qparam, int(pk), dtype, other_params

    def retrieve(self, request, *args, **kwargs):
        qparam, pk, dtype, other_params = self._init_values()

        if dtype:
            result = self.param_parser(dtype=dtype, pk=pk, **other_params)
            return Response(result)
        else:
            return super(CardsAPI, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        qparam, pk, dtype, other_params = self._init_values()
        count = int(other_params.get('count', 5))

        if dtype:
            result = self.param_parser(dtype, multi=True, **other_params)

            return Response(result)
        else:
            dset = super(CardsAPI, self).list(request, *args, **kwargs).data[:count]
            return Response(dset)

    http_method_names = ['get', 'head']

    @staticmethod
    def limit_serializer(*args):
        _list = []
        for i in args:
            musteri, limit, bakiye = i.get('musteri__firm_full_name'), i.get('limit'), i.get('bakiye')
            _dict = {
                'Müşteri': musteri,
                'Tanımlanan Limit': limit,
                'Bakiye': bakiye,
                'Limit Aşımı': limit - bakiye
            }
            _list.append(_dict)

        return _list

    @staticmethod
    def adh_serializer(*args):
        _list = []
        for i in args:
            adh_point = RiskDataSetPoints.objects.get(risk_dataset=i, variable='Devir Günü').point
            musteri, general_point = i.get('musteri__firm_full_name'), i.get('general_point')

            _dict = {
                'Müşteri': musteri,
                'ADH Skoru': general_point,
                'Risk Durumu': adh_point,
            }
            _list.append(_dict)

        return _list

    def limit_bakiye(self, dataset_id, multi=False, **kwargs):
        """
        Müşteri, Limit ve Limit - Bakiye
        :param multi: List or retrieve
        :param dataset_id:
        :return:
        """
        if multi:
            count = int(kwargs.get('count', 5))
            dataset = DataSetModel.objects.limit_asimi().values('musteri__firm_full_name',
                                                                'limit',
                                                                'bakiye')[:count]

        else:
            dataset = DataSetModel.objects.get(pk=dataset_id, **kwargs)
            dataset = {
                'musteri__firm_full_name': dataset.musteri.firm_full_name,
                'limit': dataset.limit,
                'bakiye': dataset.bakiye
            }

        return self.limit_serializer(dataset)

    def adh(self, dataset_id: int, multi=False, comp='dhself', **kwargs):
        """
        Müşteri, ADH Skoru, Risk Durumu
        :param comp: Kendi ile mi karşılaştıralım başkalarıyla mı? -> dhself || dhothers
        :param multi: List || Retrieve
        :param dataset_id:
        :param ay: 1 veya 12 olabilir
        :return:
        """

        if multi:
            count = int(kwargs.get('count', 5))
            dataset = DataSetModel.objects.asim_yapanlar(dtype=comp).values('musteri__firm_full_name',
                                                                            'general_point')[:count]
        else:
            try:
                dataset = DataSetModel.objects.asim_yapanlar(dtype=comp).get(pk=dataset_id, **kwargs)
                dataset = {
                    'musteri__firm_full_name': dataset.musteri.firm_full_name,
                    'general_point': dataset.general_point
                }

            except DataSetModel.DoesNotExist:
                raise APINoDataException

        return self.adh_serializer(dataset)

    def son_eklenen_musteriler(self, **kwargs):
        data = DataSetModel.objects.filter(**kwargs).order_by('-created_date').values('limit',
                                                                                      'teminat_durumu',
                                                                                      'musteri__firm_full_name')
        _dict = [
            {'Müşteri': k.get('musteri__firm_full_name'),
             'Tanımlanan Limit': k.get('limit'),
             'Teminat Durumu': k.get('teminat_durumu')}
            for k in data
        ]
        return data


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


class APIUsageError(APIException):
    status_code = 500
    default_detail = 'Dtype olarak ym veriyorsanız pk belirtmenize gerek yok. Son eklenen müşteriler çekilecek.' \
                     'Ama diğer tüm olasılıklar için pk belirtmeniz gerek !'


class APINoDataException(APIException):
    status_code = 500
    default_detail = 'Verdiğiniz id ile bir risk dataset objesi bulunamamıştır !'
