from django.db import models

# Create your models here.


class BaseManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    last_irrigation_date = models.DateTimeField(blank=True, verbose_name="Date", default=None, null=True)

    objects = BaseManager()

    def __str__(self):
        return self.name
