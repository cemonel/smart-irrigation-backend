from django.conf import settings
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from smart_irrigation.data.models import Data
from smart_irrigation.plant.models import Plant
from smart_irrigation.data.serializers import DataSerializer
from smart_irrigation.plant.serializers import PlantSerializer, PlantDetailSerializer


class PlantDataDetailView(ListAPIView):

    serializer_class = DataSerializer

    def get_queryset(self):
        last_week_data = Data.objects.annotate(id_mod=F('id') % 1800).filter(id_mod=0).order_by('-date')[:settings.SENSOR_FREQUENCY*60*24*7]  # Last 7 days and 1 hour time interval
        return last_week_data


class PlantDetailView(RetrieveAPIView):

    serializer_class = PlantDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        plant = Plant.objects.filter(id=self.kwargs["id"])
        return plant


class PlantListView(ListAPIView):
    serializer_class = PlantSerializer

    def get_queryset(self):
        plants = Plant.objects.all()
        return plants
