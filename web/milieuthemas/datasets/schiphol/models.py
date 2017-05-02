from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins
from datasets.themas.models import Thema


class MaatgevendeToetshoogte(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geometrie_polygon = geo.MultiPolygonField(null=False, dim=3, srid=28992)
    hoogte_nap = models.FloatField(null=False)
    hoogte_nap_klasse = models.IntegerField(null=False)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified']


class HoogtebeperkendeVlakken(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    thema = models.ForeignKey(Thema, null=True)
    bouwhoogte = models.CharField(max_length=20, null=True)
    helling = models.CharField(max_length=50, null=True)
    geometrie_point = geo.PointField(null=True, srid=28992)
    geometrie_line = geo.LineStringField(null=True, srid=28992)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified', 'thema']
    geo_view_include = ['thema_id']


class HoogtebeperkingRadar(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geometrie_polygon = geo.MultiPolygonField(null=False, dim=3, srid=28992)
    hoogte_nap = models.FloatField(null=False)
    hoogte_nap_klasse = models.IntegerField(null=False)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified']


class Geluidzone(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    thema = models.ForeignKey(Thema, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified', 'thema']
    geo_view_include = ['thema_id']


class Vogelvrijwaringsgebied(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=True)
    thema = models.ForeignKey(Thema, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified', 'thema']
    geo_view_include = ['thema_id']
