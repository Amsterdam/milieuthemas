# Project
from django.db import models
# from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins

from django.contrib.gis.db import models as geo

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import MultiPolygon


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


#class BrisantbomOnderzoek(mixins.ImportStatusMixin):
#    datum = models.DateField(null=True)
#    detectie = models.NullBooleanField()
#    Onderzoekbureau = models.CharField(max_length=32, null=True)
#    opdrachtgever = models.CharField(max_length=64, null=True)

