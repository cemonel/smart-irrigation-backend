from smart_irrigation.plant.models import Plant
from django.db import models


class BaseManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name="Plant", related_name="data")
    air_temperature = models.FloatField(blank=True, verbose_name="Air Temperature")
    air_humidity = models.FloatField(blank=True, verbose_name="Air Humidity")
    soil_moisture = models.IntegerField(blank=True, verbose_name="Soil Moisture")
    epoch = models.BigIntegerField(blank=True, verbose_name='Epoch Time')
    date = models.DateTimeField(blank=True, verbose_name="Date")

    objects = BaseManager

    class Meta:
        verbose_name_plural = 'Data'

    def __str__(self):
        return str(self.date)
