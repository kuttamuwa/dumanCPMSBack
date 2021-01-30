from avatar.models import Avatar
from rest_framework import serializers

from appconfig.models.models import Domains, Subtypes


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domains
        fields = '__all__'


class SubtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtypes
        fields = '__all__'


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'
