from rest_framework import serializers

from riskanalysis.models.models import DataSetModel, RiskDataSetPoints


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetModel
        fields = '__all__'


class RiskPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDataSetPoints
        fields = '__all__'
