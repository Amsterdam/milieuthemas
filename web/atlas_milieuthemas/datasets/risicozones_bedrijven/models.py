# Project
from django.db import models
from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins


class LPGStation(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    id = models.IntegerField(primary_key=True)
    dossiernummer = models.CharField(max_length=40, null=True)
    bedrijfsnaam = models.CharField(max_length=40, null=True)
    adres = models.CharField(max_length=100, null=True)
    postcode = models.CharField(max_length=10, null=True)
    plaats = models.CharField(max_length=15, null=True)
    stadsdeel = models.CharField(max_length=10, null=True)
    oliemaatschappij = models.CharField(max_length=10, null=True)
    omzet = models.CharField(max_length=10, null=True)
    ligging = models.CharField(max_length=20, null=True)
    tank_aanwezig = models.CharField(max_length=3, null=True)
    tank_positie = models.CharField(max_length=20, null=True)
    tank_inhoud = models.CharField(max_length=10, null=True)
    vulpunt_aanwezig = models.CharField(max_length=3, null=True)
    vulmoment = models.CharField(max_length=20, null=True)
    opmerkingen = models.TextField(null=True)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)
    geometrie_point = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()


class LPGVulpunt(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    station = models.ForeignKey(LPGStation, null=True)
    type = models.CharField(max_length=40, null=True)
    afstandseis = models.CharField(max_length=10, null=True)
    voldoet = models.CharField(max_length=3, null=True)
    geometrie_point = geo.PointField(null=True, srid=28992)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified', 'station']
    geo_view_include = ['station_id']


class LPGAfleverzuil(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    station = models.ForeignKey(LPGStation, null=True)
    geometrie_point = geo.PointField(null=True, srid=28992)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified', 'station']
    geo_view_include = ['station_id']


class LPGTank(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    station = models.ForeignKey(LPGStation, null=True)
    kleur = models.IntegerField(null=True)
    type = models.CharField(max_length=40, null=True)
    voldoet = models.CharField(max_length=3, null=True)
    afstandseis = models.CharField(max_length=10, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    geo_view_exclude = ['date_modified', 'station']
    geo_view_include = ['station_id']


class Bron(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    bron_id = models.IntegerField(null=True)
    bedrijfsnaam = models.CharField(max_length=64, null=True)
    hoeveelheid_stof = models.CharField(max_length=32, null=True)
    type_stof = models.CharField(max_length=64, null=True)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()
    
    def __repr__(self):
        return '<Bron %d: %s>' % (self.id, self.bedrijfsnaam)


class Bedrijf(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    bedrijfsnaam = models.CharField(max_length=64, null=True)
    adres = models.CharField(max_length=100, null=True)
    stadsdeel = models.CharField(max_length=16, null=True)
    aantal_bronnen = models.PositiveSmallIntegerField(null=True)
    bevoegd_gezag = models.CharField(max_length=32, null=True)
    categorie_bevi = models.CharField(max_length=100, null=True)
    type_bedrijf = models.CharField(max_length=100, null=True)
    opmerkingen = models.TextField(null=True)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    def __repr__(self):
        return '<Bedrijf %d: %s>' % (self.id, self.bedrijfsnaam)
