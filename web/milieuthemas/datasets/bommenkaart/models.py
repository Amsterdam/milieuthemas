from django.contrib.gis.db import models as geo
from django.db import models

from datapunt_generic.generic import mixins


class BomInslag(mixins.ImportStatusMixin):
    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=300, null=True)

    bron = models.CharField(max_length=300, null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)

    datum = models.DateField(null=True)

    opmerkingen = models.TextField(null=True)
    oorlogsinc = models.CharField(max_length=200)
    pdf = models.CharField(max_length=200)
    intekening = models.CharField(max_length=200)

    geometrie_point = geo.PointField(null=True, srid=28992)


class BomInslagDBView(models.Model):
    class Meta:
        managed = False
        db_table = 'geo_bommenkaart_bominslag_point'

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=300, null=True)
    bron = models.CharField(max_length=300, null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)
    datum = models.DateField(null=True)
    opmerkingen = models.TextField(null=True)
    oorlogsinc = models.CharField(max_length=200)
    pdf = models.CharField(max_length=200)
    geometrie = geo.PointField(null=True, srid=28992)
    id = models.IntegerField(primary_key=True)
    uri = models.TextField(max_length=300)
    intekening = models.CharField(max_length=200)


class GevrijwaardGebied(mixins.ImportStatusMixin):
    bron = models.CharField(max_length=200, null=True)

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=200, null=True)
    datum = models.DateField(null=True)
    opmerkingen = models.TextField(null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)
    intekening = models.CharField(max_length=200)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)


class GevrijwaardGebiedDbView(models.Model):
    class Meta:
        managed = False
        db_table = 'geo_bommenkaart_gevrijwaardgebied_polygon'

    bron = models.CharField(max_length=200, null=True)
    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=200, null=True)
    datum = models.DateField(null=True)
    opmerkingen = models.TextField(null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)
    intekening = models.CharField(max_length=200)
    id = models.IntegerField(primary_key=True)
    uri = models.TextField(max_length=300)


class VerdachtGebied(mixins.ImportStatusMixin):
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
    opmerkingen = models.TextField(null=True)

    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)


class VerdachtGebiedDbView(models.Model):
    class Meta:
        managed = False
        db_table = 'geo_bommenkaart_verdachtgebied_polygon'

    bron = models.CharField(max_length=200, null=True)
    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=200, null=True)
    subtype = models.CharField(max_length=200, null=True)
    aantal = models.CharField(max_length=200, null=True)
    kaliber = models.CharField(max_length=200, null=True)
    verschijning = models.CharField(max_length=200, null=True)
    oorlogshandeling = models.CharField(max_length=200, null=True)
    afbakening = models.CharField(max_length=200, null=True)
    horizontaal = models.CharField(max_length=200, null=True)
    cartografie = models.CharField(max_length=200, null=True)
    pdf = models.CharField(max_length=200)
    id = models.IntegerField(primary_key=True)
    uri = models.TextField(max_length=300)
    opmerkingen = models.TextField(max_length=300)


class UitgevoerdOnderzoek(mixins.ImportStatusMixin):
    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=200, null=True)
    datum = models.DateField(null=True)
    onderzoeksgebied = models.CharField(max_length=200, null=True)
    opdrachtgever = models.CharField(max_length=200, null=True)
    opdrachtnemer = models.CharField(max_length=200, null=True)
    verdacht_gebied = models.CharField(max_length=200, null=True)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)


class UitgevoerdOnderzoekDbView(models.Model):
    class Meta:
        managed = False
        db_table = 'geo_bommenkaart_uitgevoerdonderzoek_polygon'

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=200, null=True)
    datum = models.DateField(null=True)
    onderzoeksgebied = models.CharField(max_length=200, null=True)
    opdrachtgever = models.CharField(max_length=200, null=True)
    opdrachtnemer = models.CharField(max_length=200, null=True)
    verdacht_gebied = models.CharField(max_length=200, null=True)
    id = models.IntegerField(primary_key=True)
    uri = models.TextField(max_length=300)
