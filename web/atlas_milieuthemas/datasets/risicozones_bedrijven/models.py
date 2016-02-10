from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins


class LPGVulpunt(mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    stationnummer = models.IntegerField(null=True)
    type = models.CharField(max_length=40, null=True)
    afstandseis = models.CharField(max_length=10, null=True)
    voldoet = models.CharField(max_length=3, null=True)
    geometrie_point = geo.PointField(null=True, srid=28992)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()
