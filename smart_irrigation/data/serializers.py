import datetime

from rest_framework import serializers

from smart_irrigation.data.models import Data


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = (
            'id',
            'air_temperature',
            'air_humidity',
            'soil_moisture',
            'date',
        )
