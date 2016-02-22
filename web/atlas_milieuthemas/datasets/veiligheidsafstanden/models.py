from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins
from datasets.themas.models import Thema


class Veiligheidsafstand(mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    thema = models.ForeignKey(Thema, null=True)
    locatie = models.CharField(max_length=100, null=True)
    geometrie_multipolygon = geo.MultiPolygonField(null=True, srid=28992)
    geometrie_point = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()
