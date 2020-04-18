import datetime

from rest_framework import serializers

from smart_irrigation.data.models import Data


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = (
            'id',
            'plant',
            'air_temperature',
            'air_humidity',
            'soil_moisture',
            'date',
        )

    def validate_date(self, date):
        ts_epoch = date
        return datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')

