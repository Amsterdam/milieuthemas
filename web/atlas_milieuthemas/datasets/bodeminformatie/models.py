from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins


class Grondmonster(mixins.ImportStatusMixin):
    geo_id = models.IntegerField(null=False)
    locatie = models.CharField(max_length=100, null=True)
    am_nummer = models.CharField(max_length=40, null=True)
    type_onderzoek = models.CharField(max_length=40, null=True)
    rapportnummer = models.CharField(max_length=40, null=True)
    bureau = models.CharField(max_length=100, null=True)
    rapportdatum = models.DateField(null=True)
    naam_boring = models.CharField(max_length=40)
    xcoordinaat = models.IntegerField(null=True)
    ycoordinaat = models.IntegerField(null=True)
    grondwaterstand = models.IntegerField(null=True)
    naam_monster = models.CharField(max_length=40, null=True)
    materiaal = models.CharField(max_length=40, null=True)
    bovenkant = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    onderkant = models.IntegerField(null=True)
    eindoordeel = models.CharField(max_length=4, null=True)
    monster_mengmonster = models.CharField(max_length=20, null=True)
    lutum = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    organische_stof = models.IntegerField(null=True)
    cadmium = models.IntegerField(null=True)
    kwik = models.IntegerField(null=True)
    koper = models.IntegerField(null=True)
    nikkel = models.IntegerField(null=True)
    lood = models.IntegerField(null=True)
    zink = models.IntegerField(null=True)
    chroom = models.IntegerField(null=True)
    arseen = models.IntegerField(null=True)
    pak = models.IntegerField(null=True)
    eox = models.IntegerField(null=True)
    pcb = models.IntegerField(null=True)
    minerale_olie = models.IntegerField(null=True)
    geometrie = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()
