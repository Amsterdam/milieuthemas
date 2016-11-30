# Project
from django.db import models
# from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins


class Brisantbom(mixins.ImportStatusMixin):
    id = models.IntegerField(primary_key=True)
    bron = models.CharField(max_length=100, null=True)
    datum_inslag = models.DateField(null=True)
    exact = models.NullBooleanField()
    geruimd = models.NullBooleanField()
    kaliber = models.CharField(max_length=32, null=True)
    omschrijving = models.TextField(null=True)


class BrisantbomOnderzoek(mixins.ImportStatusMixin):
    datum = models.DateField(null=True)
    detectie = models.NullBooleanField()
    Onderzoekbureau = models.CharField(max_length=32, null=True)
    opdrachtgever = models.CharField(max_length=64, null=True)
    