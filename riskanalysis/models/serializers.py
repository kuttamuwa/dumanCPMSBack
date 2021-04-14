from rest_framework import serializers

from checkaccount.models.models import CheckAccount
from checkaccount.models.serializers import CheckAccountSerializer
from riskanalysis.models.models import DataSetModel, RiskDataSetPoints


class DatasetSerializerGeneral(serializers.ModelSerializer):
    musteri = serializers.PrimaryKeyRelatedField(
        queryset=CheckAccount.objects.all(),
        source='musteri.firm_full_name'
    )

    class Meta:
        model = DataSetModel
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        validated_data['musteri'] = validated_data['musteri']['firm_full_name']
        return DataSetModel.objects.get_or_create(**validated_data)


class DatasetSerializerExclusive(serializers.ModelSerializer):
    musteri = serializers.CharField(source='musteri.firm_full_name', read_only=True)

    class Meta:
        model = DataSetModel
        fields = '__all__'


class RiskPointsSerializer(serializers.ModelSerializer):
    musteri = serializers.CharField(source='musteri.firm_full_name')

    class Meta:
        model = RiskDataSetPoints
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    musteri = serializers.CharField(source='musteri.firm_full_name')

    class Meta:
        model = DataSetModel
        fields = '__all__'


class RiskPointsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDataSetPoints
        fields = ('risk_dataset', 'point', 'data_id')


class RiskPointsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDataSetPoints
        fields = ('risk_dataset',)
