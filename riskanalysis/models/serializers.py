from rest_framework import serializers

from riskanalysis.models.models import DataSetModel, RiskDataSetPoints


class DatasetSerializerGeneral(serializers.ModelSerializer):
    musteri = serializers.CharField(source='musteri.firm_full_name')

    class Meta:
        model = DataSetModel
        fields = '__all__'


class DatasetSerializerLimited(serializers.ModelSerializer):
    firm_full_name = serializers.ReadOnlyField(source='musteri.firm_full_name')
    taxpayer_number = serializers.ReadOnlyField(source='musteri.taxpayer_number')

    class Meta:
        model = DataSetModel
        fields = ('data_id', 'firm_full_name', 'general_point', 'taxpayer_number')


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
        fields = ('risk_dataset',)
