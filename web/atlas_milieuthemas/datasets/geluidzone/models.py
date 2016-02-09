from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins
from datasets.themas.models import Thema


class GeluidzoneAbstract(mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    thema = models.ForeignKey(Thema, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    class Meta:
        abstract = True


class Spoorwegen(GeluidzoneAbstract):
    pass


class Metro(GeluidzoneAbstract):
    pass


class Industrie(GeluidzoneAbstract):
    naam = models.CharField(max_length=100, null=True)
