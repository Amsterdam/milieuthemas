# Project
from django.db import models
# from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins

from django.contrib.gis.db import models as geo


class BomInslag(mixins.ModelViewFieldsMixin,
                mixins.ImportStatusMixin):

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=300, null=True)

    bron = models.CharField(max_length=300, null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)

    datum = models.DateField(null=True)

    opmerkingen = models.TextField(null=True)
    oorlogsinc = models.CharField(max_length=200)
    pdf = models.CharField(max_length=200)

    geometrie_point = geo.PointField(null=True, srid=28992)


class GevrijwaardGebied(
        mixins.ModelViewFieldsMixin,
        mixins.ImportStatusMixin):

    bron = models.CharField(max_length=200, null=True)

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=200, null=True)
    datum = models.DateField(null=True)
    opmerkingen = models.TextField(null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)


class VerdachtGebied(
        mixins.ModelViewFieldsMixin,
        mixins.ImportStatusMixin):

    bron = models.CharField(max_length=200, null=True)

    kenmerk = models.CharField(max_length=32)
    # hoofdgroep
    type = models.CharField(max_length=200, null=True)
    # subsoort
    subtype = models.CharField(max_length=200, null=True)

    aantal = models.CharField(max_length=200, null=True)
    kaliber = models.CharField(max_length=200, null=True)
    verschijning = models.CharField(max_length=200, null=True)

    oorlogshandeling = models.CharField(max_length=200, null=True)
    afbakening = models.CharField(max_length=200, null=True)

    horizontaal = models.CharField(max_length=200, null=True)
    cartografie = models.CharField(max_length=200, null=True)
    pdf = models.CharField(max_length=200)

    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)


class UitgevoerdOnderzoek(
        mixins.ModelViewFieldsMixin,
        mixins.ImportStatusMixin):

    kenmerk = models.CharField(max_length=32)

    type = models.CharField(max_length=200, null=True)

    datum = models.DateField(null=True)

    onderzoeksgebied = models.CharField(max_length=200, null=True)

    opdrachtgever = models.CharField(max_length=200, null=True)
    opdrachtnemer = models.CharField(max_length=200, null=True)

    verdacht_gebied = models.CharField(max_length=200, null=True)

    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)
