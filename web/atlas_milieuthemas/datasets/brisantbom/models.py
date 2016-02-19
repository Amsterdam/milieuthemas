# Project
from django.db import models
# from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins


class Brisantbom(mixins.ImportStatusMixin):
    bron = models.CharField(max_length=100, null=True)
    datum_inslag = models.DateField(null=True)
    exact = models.NullBooleanField()
    geruimd = models.NullBooleanField()
    kaliber = models.CharField(max_length=32, null=True)  # TODO this can probably be a choice field. need to talk to Jeroen
    omschrijving = models.TextField(null=True)
