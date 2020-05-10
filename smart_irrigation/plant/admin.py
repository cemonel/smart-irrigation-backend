# Register your models here.

from django.contrib import admin

from smart_irrigation.plant.models import Plant


# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_irrigation_date', 'status', 'irrigation_count')


admin.site.register(Plant, PlantAdmin)
