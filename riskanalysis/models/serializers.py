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


class RiskPointsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDataSetPoints
        fields = ('risk_dataset', 'point', 'data_id')


class RiskPointsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDataSetPoints
        fields = ('risk_dataset', )


