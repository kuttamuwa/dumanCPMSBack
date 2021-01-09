from rest_framework import serializers

from riskanalysis.models.models import DataSetModel, RiskDataSetPoints


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetModel


class RiskPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDataSetPoints

