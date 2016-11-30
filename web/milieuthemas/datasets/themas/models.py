from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins


class Thema(mixins.ImportStatusMixin):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=100, null=True)
    toelichting = models.TextField(null=True)
    wet_of_regelgeving = models.CharField(max_length=255, null=True)
    datum_laatste_wijziging = models.CharField(max_length=20, null=True)
    disclaimer = models.TextField(null=True)
    informatie = geo.CharField(max_length=100, null=True)

    def __str__(self):
        return '{}'.format(self.type)
