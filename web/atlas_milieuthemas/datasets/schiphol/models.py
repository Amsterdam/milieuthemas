from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins


class HoogtebeperkendeVlakken(mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    tma_id = models.SmallIntegerField(null=True)
    bouwhoogte = models.CharField(max_length=20, null=True)
    helling = models.CharField(max_length=50, null=True)
    geometrie_point = geo.PointField(null=True, srid=28992)
    geometrie_line = geo.LineStringField(null=True, srid=28992)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()
