from rest_framework import viewsets

from riskanalysis.models.models import DataSetModel
from riskanalysis.models.serializers import DatasetSerializer


class RiskAnalysisApi(viewsets.ReadOnlyModelViewSet):
    """
    * Istenen veri tipi: -> :param dtype

        * Vade -> ?dtype=v
        * Devir Hızı :
            * self -> ?dype=dh1
            * baskalariyla -> ?dype=dh2
        * Limit -> ?dtype=l

        * İade aşımı yapanlar:
            * self -> ?dtype=i1
            * baskalariyla -> ?dtype=i2

        * SGK Borcu olanlar -> ?dtype=s

        * Sektör Kara Listede olanlar -> ?dtype=skl

        dtype_list = {'v': self._vade_asimi,
                      'dh1': self._devir_hizi_self_artmis,
                      'dh2': self._devir_hizi_self_artmis,
                      'l': self._limit_asimi,
                      'i1': self._iade_self_artis,
                      'i2': self._iade_baskalariyla_artis
                      's': self._sgk_borcu_olanlar,
                      'skl': self._sektor_kara_liste}

    """
    queryset = DataSetModel.objects.all()
    serializer_class = DatasetSerializer

    def get_queryset(self):
        print("istek geldi")
        dtype = self.request.GET.get('dtype', None)
        if dtype is not None:
            return DataSetModel.objects.asim_yapanlar(dtype)


# class ExternalDataApi:
#     """
#     * Vergi
#     * SGK
#     * Sektör Kara Liste
#     * Findeks Kredi Notu
#     * Karekodlu Çek Skoru
#
#     """
#     pass


# class CheckAccountDataApi(RetrieveAPIView):
#     """
#     * Son eklenen müşteriler
#     """
#     queryset = CheckAccount
#     serializer_class = CheckAccountSerializer
#
#     def get_queryset(self):
#         return super(CheckAccountDataApi, self).get_queryset()

