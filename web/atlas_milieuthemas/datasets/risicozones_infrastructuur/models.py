# Project
from django.db import models
from django.contrib.gis.db import models as geo
# Product
from datapunt_generic.generic import mixins


class Aardgasleiding(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    """
    Aardgasleiding model holds the geometry information for
    the actual gas lines
    """
    geometrie = geo.MultiLineStringField(null=True, srid=28992)


class AardgasGebied(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    """
    AardgasRisico model holds risico zones associated with aardgas.
    LET_100 - 100% fatality zone
    LET_1 - 1% Fatality zone
    ZAKELIJK - Bedrijf consideration zone
    PLAATSGEBONDEN_RISICO - Unclear
    """
    LET_100 = 'la'
    LET_1 = 'l1'
    ZAKELIJK = 'zk'
    PLAATSGEBONDEN_RISICO = 'pr'
    AARDGAS_LEIDING_CHOICIES = (
        (LET_100, 'Letaliteitsafstand 100'),
        (LET_1, 'Letaliteitsafstand 1'),
        (ZAKELIJK, 'Belemmeringenstrook'),
        (PLAATSGEBONDEN_RISICO, 'Plaatsgebonden risico'),
    )
    type = models.CharField(max_length=2, choices=AARDGAS_LEIDING_CHOICIES, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)


class Infrastructuur(mixins.ModelViewFieldsMixin, mixins.ImportStatusMixin):
    SPOORWEG = 'sw'
    VAARWEGEN = 'vw'
    WEGEN = 'wg'
    INFRASTRUCTUUR_TYPE_CHOICES = (
        (SPOORWEG, 'Spoorweg'),
        (VAARWEGEN, 'Vaarweg'),
        (WEGEN, 'Weg'),
    )
    type = models.CharField(max_length=2, choices=INFRASTRUCTUUR_TYPE_CHOICES, null=True)
    geometrie = geo.MultiPolygonField(null=True, srid=28992)

    objects = geo.GeoManager()

    def __repr__(self):
        """
        To make it clearer what the content is,
        making a custom repr
        """
        return "<Infrastructuur {0}: {1}>".format(self.id, self.type)
