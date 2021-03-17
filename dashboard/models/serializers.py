from rest_framework import serializers

from riskanalysis.models.models import DataSetModel


class DatasetSerializerGeneral(serializers.ModelSerializer):
    class Meta:
        model = DataSetModel
        fields = '__all__'


class DatasetSerializerLimited(serializers.ModelSerializer):
    firm_full_name = serializers.ReadOnlyField(source='musteri.firm_full_name')
    taxpayer_number = serializers.ReadOnlyField(source='musteri.taxpayer_number')

    class Meta:
        model = DataSetModel
        fields = ('data_id', 'firm_full_name', 'general_point', 'taxpayer_number')
