from django.contrib.gis.db import models as geo
from django.db import models

from datapunt_generic.generic import mixins


class BomInslag(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=128, null=True)  # Dataset/data type
    detail_type = models.CharField(max_length=300, null=True)
    bron = models.CharField(max_length=300, null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)

    datum = models.DateField(null=True)
    datum_inslag = models.DateField(null=True)

    opmerkingen = models.TextField(null=True)
    oorlogsinc = models.CharField(max_length=200)
    pdf = models.CharField(max_length=200)
    intekening = models.CharField(max_length=200)

    geometrie_point = geo.PointField(null=True, srid=28992)

    # Geoview settings
    display_field = 'kenmerk'
    geo_view_exclude = ['pdf']
    url_path = 'milieuthemas/explosieven/inslagen/'


class GevrijwaardGebied(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    bron = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=128, null=True)  # Dataset/data type
    kenmerk = models.CharField(max_length=32)
    detail_type = models.CharField(max_length=255, null=True)

    datum = models.DateField(null=True)

    opmerkingen = models.TextField(null=True)
    nauwkeurig = models.CharField(max_length=200, null=True)
    intekening = models.CharField(max_length=200)

    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    # Geoview settings
    display_field = 'kenmerk'
    url_path = 'milieuthemas/explosieven/gevrijwaardgebied/'

class VerdachtGebied(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    bron = models.CharField(max_length=200, null=True)

    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=128, null=True)  # Dataset/data type
    # hoofdgroep
    detail_type = models.CharField(max_length=255, null=True)
    # subsoort
    subtype = models.CharField(max_length=255, null=True)

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

    # Geoview settings
    display_field = 'kenmerk'
    geo_view_exclude = ['pdf']
    url_path = 'milieuthemas/explosieven/verdachtgebied/'


class UitgevoerdOnderzoek(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    kenmerk = models.CharField(max_length=32)
    type = models.CharField(max_length=128, null=True)  # Dataset/data type
    detail_type = models.CharField(max_length=255, null=True)

    datum = models.DateField(null=True)

    onderzoeksgebied = models.CharField(max_length=200, null=True)
    opdrachtgever = models.CharField(max_length=200, null=True)
    opdrachtnemer = models.CharField(max_length=200, null=True)
    verdacht_gebied = models.CharField(max_length=200, null=True)

    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    # Geoview settings
    display_field = 'kenmerk'
    url_path = 'milieuthemas/explosieven/uitgevoerdonderzoek/'
