from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from riskanalysis.models.models import DataSetModel, RiskDataSetPoints
from riskanalysis.models.serializers import RiskPointsSerializer, DatasetSerializer
from riskanalysis.views.permissions import DatasetPermission, RiskPointsPermission


class DatasetAPI(viewsets.ModelViewSet):
    queryset = DataSetModel.objects.all().order_by('-created_date')
    serializer_class = DatasetSerializer

    permission_classes = [IsAuthenticated, DatasetPermission]


class RiskPointsAPI(viewsets.ModelViewSet):
    queryset = RiskDataSetPoints.objects.all().order_by('-created_date')
    serializer_class = RiskPointsSerializer
    permission_classes = [IsAuthenticated, RiskPointsPermission]
