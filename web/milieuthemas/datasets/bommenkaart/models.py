# Project
from django.db import models
# from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins

from django.contrib.gis.db import models as geo


class BomInslag(mixins.ModelViewFieldsMixin,
                mixins.ImportStatusMixin):

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=100, null=True)

    bron = models.CharField(max_length=100, null=True)
    nauwkeurig = models.CharField(max_length=100, null=True)

    datum = models.DateField(null=True)

    opmerkingen = models.TextField(null=True)
    oorlogsinc = models.CharField(max_length=200)
    pdf = models.CharField(max_length=200)

    geometrie_point = geo.PointField(null=True, srid=28992)


class GevrijwaardGebied(
        mixins.ModelViewFieldsMixin,
        mixins.ImportStatusMixin):

    bron = models.CharField(max_length=100, null=True)

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=100, null=True)
    datum = models.DateField(null=True)
    opmerkingen = models.TextField(null=True)
    nauwkeurig = models.CharField(max_length=100, null=True)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)
