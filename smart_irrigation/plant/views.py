import datetime

from django.db.models import F
from django.utils.timezone import timedelta, now

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from smart_irrigation.data.models import Data
from smart_irrigation.plant.models import Plant
from smart_irrigation.data.serializers import DataSerializer
from smart_irrigation.plant.serializers import PlantSerializer, PlantDetailSerializer, PlantIrrigationSerializer


class PlantDataDetailView(ListAPIView):

    serializer_class = DataSerializer
    lookup_field = "id"

    def get_queryset(self):
        last_data = Data.objects.all().order_by("-date")[0]
        data = Data.objects.filter(id=last_data.id)
        last_week_data = Data.objects.annotate(id_mod=F('id') % 60).filter(id_mod=0, plant_id=self.kwargs["id"]).order_by('date')  # last 1 weeks data
        last_week_data = last_week_data.filter(date__gte=now() - timedelta(days=7))
        return data | last_week_data


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


class PlantIrrigationView(APIView):

    def get(self, request, *args, **kwargs):
        plant = Plant.objects.get(id=self.kwargs["id"])
        if plant.status == Plant.STATUS_IRRIGATE:
            plant.status = Plant.STATUS_WAIT
            plant.save()
            return Response({"status": "Irrigate"})
        else:
            return Response({"status": "Wait"})


class IrrigatePlantView(APIView):

    def get(self, request, *args, **kwargs):
        plant = Plant.objects.get(id=self.kwargs["id"])
        plant.status = Plant.STATUS_IRRIGATE
        plant.irrigation_count = plant.irrigation_count + 1
        plant.last_irrigation_date = datetime.datetime.now()
        plant.save()
        return Response()
