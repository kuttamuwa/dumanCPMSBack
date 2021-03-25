from rest_framework import serializers
from checkaccount.models.models import CheckAccount, SysPersonnel, Sectors, Cities, Districts


class CheckAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckAccount
        fields = '__all__'

    def update(self, instance, validated_data):
        return super(CheckAccountSerializer, self).update(instance, validated_data)


class SysPersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysPersonnel
        fields = '__all__'


class SectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sectors
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')

    class Meta:
        model = Districts
        fields = '__all__'
