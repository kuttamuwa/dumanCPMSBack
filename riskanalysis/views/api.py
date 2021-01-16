from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.models.serializers import RiskPointsSerializer, DatasetSerializer, RiskPointsGetSerializer, RiskPointsPostSerializer
from riskanalysis.views.permissions import DatasetPermission, RiskPointsPermission


class DatasetAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = DatasetSerializer

    permission_classes = [IsAuthenticated, DatasetPermission]


class RiskPointsAPI(viewsets.ModelViewSet):
    queryset = RiskDataSetPoints.objects.all().order_by('-created_date')
    serializer_class = RiskPointsSerializer  # general serializer
    permission_classes = [IsAuthenticated, RiskPointsPermission]
    lookup_field = 'data_id'

    @staticmethod
    def test_create_point():
        rd = DataSetModel.objects.first()
        pnt = RiskDataSetPoints(risk_dataset=rd, variable='TOPLAM', point=47.4)
        pnt.save()

    def __get_riskdataset(self, **kwargs):
        return DataSetModel.objects.filter(**kwargs)

    def get_queryset(self):
        qset = super(RiskPointsAPI, self).get_queryset()
        if self.request.method == 'GET':
            self.serializer_class = RiskPointsGetSerializer
            rd = self.__get_riskdataset(**self.kwargs)
            qset = qset.filter(variable='TOPLAM', risk_dataset__in=rd)

        elif self.request.method == 'POST':
            self.serializer_class = RiskPointsPostSerializer

        return qset