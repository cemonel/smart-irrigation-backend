from django.contrib import admin

from smart_irrigation.data.models import Data
from django.conf.locale.es import formats as es_formats

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


admin.site.register(Data, DataAdmin)
