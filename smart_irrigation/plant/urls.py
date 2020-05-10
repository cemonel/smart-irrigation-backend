from django.urls import path
from django.conf.urls import url

from smart_irrigation.plant.views import PlantDataDetailView, PlantListView, PlantDetailView, PlantIrrigationView, IrrigatePlantView


urlpatterns = [
    url(r'^(?P<id>[^/]+)/data-detail/', PlantDataDetailView.as_view(), name='plant-data-detail'),
    url(r'^(?P<id>[^/]+)/detail/', PlantDetailView.as_view(), name='plant-detail'),
    url(r'^(?P<id>[^/]+)/irrigation/', PlantIrrigationView.as_view(), name='plant-irrigation'),
    url(r'^(?P<id>[^/]+)/irrigate/', IrrigatePlantView.as_view(), name='plant-irrigate'),
    url('list/', PlantListView.as_view(), name='plant-data-detail'),
]
