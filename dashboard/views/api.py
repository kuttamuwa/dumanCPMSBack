from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from dashboard.models.serializers import DatasetSerializerLimited, DatasetSerializerGeneral, DataSetModel


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
                      'dh2': self._devir_hizi_baskalariyla_artmis: Diğer müşterilerin ortalaması alınır
                      'l': self._limit_asimi,
                      'i1': self._iade_self_artis,
                      'i2': self._iade_baskalariyla_artis
                      's': self._sgk_borcu_olanlar,
                      'skl': self._sektor_kara_liste}

    """
    queryset = DataSetModel.objects.all()
    serializer_class = DatasetSerializerLimited
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        print("istek geldi")
        dtype = self.request.GET.get('dtype', None)
        limit = self.request.GET.get('limit', 5)  # default

        if dtype is not None:
            return DataSetModel.objects.asim_yapanlar(dtype)[:limit]


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

