# Project
from django.db import models
from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins


class Aardgasbuisleiding(mixins.ImportStatusMixin):
    geometrie = geo.MultiLineStringField(null=True, srid=28992)
    
    objects = geo.GeoManager()


class Spoorweg(mixins.ImportStatusMixin):
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()
