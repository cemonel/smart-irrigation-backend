from django.contrib import admin

from smart_irrigation.data.models import Data, DataSummary
from django.conf.locale.es import formats as es_formats
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import F

from django.core.serializers.json import DjangoJSONEncoder

import json
from .models import Data
from smart_irrigation.plant.models import Plant

es_formats.DATETIME_FORMAT = "d M Y H:i:s"


# Register your models here.
class DataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Details', {'fields': ('date', 'soil_moisture', 'air_temperature', 'air_humidity', 'epoch', 'plant',)}),
    ]

    list_display = ('id', 'date', 'soil_moisture', 'air_temperature', 'air_humidity', 'plant', 'epoch')

    search_fields = ('id', 'date', 'soil_moisture', 'air_temperature', 'air_humidity', 'plant', 'epoch')
    ordering = ('-date',)

    # add_fieldsets = (
    #     (
    #         None, {
    #             'classes': ('wide',),
    #             'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff')
    #         }
    #     ),
    # )


class PlantAndData(object):
    def __init__(self):
        self.data_list = []
        self.plant_name = ''


@admin.register(DataSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/data_summary_change_list.html'
    date_hierarchy = 'date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        plant_list = []

        for plant in Plant.objects.all():
            plant_object = PlantAndData()
            plant_object.data_list = list(Data.objects.filter(plant_id=plant.id).values())
            plant_object.plant_name = plant.name
            plant_list.append(plant_object.__dict__)

        item_json = json.dumps(plant_list, cls=DjangoJSONEncoder)

        response.context_data['plants'] = item_json

        min_soil = Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').first()[0]
        max_soil = Data.objects.filter().values_list('soil_moisture').order_by('soil_moisture').last()[0]

        response.context_data['min_soil'] = min_soil
        response.context_data['max_soil'] = max_soil

        return response


admin.site.register(Data, DataAdmin)
