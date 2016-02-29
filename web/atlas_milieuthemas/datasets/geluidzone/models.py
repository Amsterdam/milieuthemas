from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins
from datasets.themas.models import Thema


class GeluidzoneAbstract(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    thema = models.ForeignKey(Thema, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    class Meta:
        abstract = True

    def get_view_fields(self):
        exclude = ['date_modified', 'thema'] + self.model_geo_fields
        return ['thema_id'] + [fld for fld in self.get_model_fields() if fld not in exclude]


class Spoorwegen(GeluidzoneAbstract):
    pass


class Metro(GeluidzoneAbstract):
    pass


class Industrie(GeluidzoneAbstract):
    naam = models.CharField(max_length=100, null=True)
