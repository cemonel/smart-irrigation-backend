from rest_framework import serializers

from django.db.models import Avg

from smart_irrigation.plant.models import Plant
from smart_irrigation.data.models import Data


class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = (
            'id',
            'name',
        )


class PlantDetailSerializer(serializers.ModelSerializer):
    last_irrigation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    max_temperature = serializers.SerializerMethodField(read_only=True)
    min_temperature = serializers.SerializerMethodField(read_only=True)
    max_soil_moisture = serializers.SerializerMethodField(read_only=True)
    min_soil_moisture = serializers.SerializerMethodField(read_only=True)
    max_air_humidity = serializers.SerializerMethodField(read_only=True)
    min_air_humidity = serializers.SerializerMethodField(read_only=True)
    current_temperature = serializers.SerializerMethodField(read_only=True)
    current_soil_moisture = serializers.SerializerMethodField(read_only=True)
    current_air_humidity = serializers.SerializerMethodField(read_only=True)
    avg_air_humidity = serializers.SerializerMethodField(read_only=True)
    avg_temperature = serializers.SerializerMethodField(read_only=True)
    avg_soil_moisture = serializers.SerializerMethodField(read_only=True)
    max_soil_as_analog = serializers.SerializerMethodField(read_only=True)
    min_soil_as_analog = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Plant
        fields = (
            'id',
            'name',
            'last_irrigation_date',
            'current_temperature',
            'current_air_humidity',
            'current_soil_moisture',
            'max_temperature',
            'min_temperature',
            'max_soil_moisture',
            'min_soil_moisture',
            'max_air_humidity',
            'min_air_humidity',
            'avg_temperature',
            'avg_soil_moisture',
            'avg_air_humidity',
            'max_soil_as_analog',
            'min_soil_as_analog'
        )

    def get_max_temperature(self, max_temperature):
        max_temperature = Data.objects.filter().values_list('air_temperature').order_by('air_temperature').last()
        return max_temperature

    def get_min_temperature(self, min_temperature):
        min_temperature = Data.objects.filter().values_list('air_temperature').order_by('air_temperature').first()
        return min_temperature

    def get_max_soil_moisture(self, max_soil_moisture):
        max_soil_moisture = Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').first()
        min_soil_moisture = Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').last()

        return 100 - (max_soil_moisture[0] / (min_soil_moisture[0]) * 100)

    def get_min_soil_moisture(self, min_soil_moisture):
        min_soil_moisture = Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').last()
        return 100 - (min_soil_moisture[0] / (min_soil_moisture[0]) * 100)

    def get_max_air_humidity(self, max_air_humidity):
        max_air_humidity = Data.objects.filter().values_list('air_humidity').order_by('air_humidity').last()
        return max_air_humidity

    def get_min_air_humidity(self, min_air_humidity):
        min_air_humidity = Data.objects.filter().values_list('air_humidity').order_by('air_humidity').first()
        return min_air_humidity

    def get_current_temperature(self, current_temperature):
        return Data.objects.all().values_list('air_temperature').last()

    def get_current_soil_moisture(self, current_soil_moisture):
        min_soil_moisture = Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').last()
        return 100 - (Data.objects.all().values_list('soil_moisture').last()[0] / (min_soil_moisture[0]) * 100)

    def get_current_air_humidity(self, current_air_humidity):
        return Data.objects.all().values_list('air_humidity').last()

    def get_avg_air_humidity(self, avg_air_humidity):
        return Data.objects.aggregate(Avg('air_humidity'))

    def get_avg_temperature(self, avg_temperature):
        return Data.objects.aggregate(Avg('air_temperature'))

    def get_avg_soil_moisture(self, avg_soil_moisture):
        return Data.objects.aggregate(Avg('soil_moisture'))

    def get_max_soil_as_analog(self, max_soil_as_analog):
        return Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').first()[0]

    def get_min_soil_as_analog(self, min_soil_as_analog):
        return Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').last()[0]


class PlantIrrigationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plant
        fields = (
            'status',
            'irrigation_duration'
        )
