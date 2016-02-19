# Project
from django.db import models
from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins


class Infrastructuur(mixins.ImportStatusMixin):
    AARDGAS_LEIDING = 'ag'
    SPOORWEG = 'sw'
    VAARWEGEN = 'vw'
    WEGEN = 'wg'
    INFRASTRUCTUUR_TYPE_CHOICES = (
        (AARDGAS_LEIDING, 'Aardgasleiding'),
        (SPOORWEG, 'Spoorweg'),
        (VAARWEGEN, 'Vaarweg'),
        (WEGEN, 'Weg'),
    )
    type = models.CharField(max_length=2, choices=INFRASTRUCTUUR_TYPE_CHOICES, null=True)
    geometrie_line = geo.MultiLineStringField(null=True, srid=28992)
    geometrie_polygon = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    def __repr__(self):
        """
        To make it clearer what the content is,
        making a custom repr
        """
        return "<Infrastructuur {0}: {1}>".format(self.id, self.type)
