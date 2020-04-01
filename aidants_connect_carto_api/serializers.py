from rest_framework import serializers

from aidants_connect_carto_api.models import Place, Service


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = []


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = []
