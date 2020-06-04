from django.db import models
from location_field.models.plain import PlainLocationField
# Create your models here.


class BaseManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Plant(models.Model):

    STATUS_WAIT = "wait"
    STATUS_IRRIGATE = "irrigate"

    STATUS_CHOICES = (
        (STATUS_WAIT, "Wait"),
        (STATUS_IRRIGATE, "Irrigate"),
    )

    IRRIGATION_SURFACE = "surface"
    IRRIGATION_DRIP = "drip"
    IRRIGATION_SPRINKLER = "sprinkler"
    IRRIGATION_SUBSURFACE = "subsurface"

    IRRIGATION_CHOICES = (
        (IRRIGATION_SURFACE, "Surface"),
        (IRRIGATION_DRIP, "Drip"),
        (IRRIGATION_SPRINKLER, "Sprinkler"),
        (IRRIGATION_SUBSURFACE, "Subsurface"),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    last_irrigation_date = models.DateTimeField(blank=True, verbose_name="Last Irrigation Date", default=None, null=True)
    status = models.CharField(max_length=10, default=STATUS_WAIT, choices=STATUS_CHOICES)
    irrigation_count = models.IntegerField(default=0)
    location = PlainLocationField(based_fields=['city'], zoom=7, default=None)
    city = models.CharField(max_length=255)
    irrigation_type = models.CharField(max_length=10, default=IRRIGATION_DRIP, choices=IRRIGATION_CHOICES)
    irrigation_duration = models.IntegerField(default=5)
    machine_learning = models.BooleanField(default=True)

    objects = BaseManager()

    def __str__(self):
        return self.name
