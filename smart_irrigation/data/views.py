from datetime import datetime
import pytz

from rest_framework.views import APIView
from rest_framework.response import Response

from smart_irrigation.data.models import Data
from smart_irrigation.data.models import Plant


# Create your views here.
def convert_epoch_to_datetime(t):
    local_tz = pytz.timezone("Asia/Istanbul")
    utc_dt = datetime.utcfromtimestamp(t).replace(tzinfo=pytz.utc)
    return local_tz.normalize(utc_dt.astimezone(local_tz))


class CreateDataView(APIView):

    def get(self, request):
        plant = Plant.objects.first()
        data = Data(plant=plant)
        data.epoch = int(request.query_params['time'])
        data.date = convert_epoch_to_datetime(int(request.query_params['time']))
        data.air_humidity = float(request.query_params['air_humidity'])
        data.air_temperature = float(request.query_params['air_temperature'])
        data.soil_moisture = int(request.query_params['soil_moisture'])

        data.save()

        return Response(status=200)

