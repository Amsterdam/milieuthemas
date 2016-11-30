import factory
from factory import fuzzy

from django.contrib.gis.geos import Point, MultiPolygon, Polygon

from .. import models

multipoly = MultiPolygon(
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
)


class IdMixin(factory.DjangoModelFactory):
    id = fuzzy.FuzzyInteger(1, 10)


# station
class LPGStationBase(IdMixin):
    bedrijfsnaam = fuzzy.FuzzyText(length=40)
    dossiernummer = fuzzy.FuzzyText(length=40)

    class Meta:
        model = models.LPGStation


class LPGStationPointFactory(LPGStationBase):
    geometrie_point = Point(0.0, 1.1)


class LPGStationPolygonFactory(LPGStationBase):
    geometrie_polygon = multipoly


# vulpunt
class LPGVulpuntBase(IdMixin):
    geo_id = fuzzy.FuzzyInteger(1, 10)
    type = fuzzy.FuzzyText(length=40)
    afstandseis = fuzzy.FuzzyText(length=10)
    voldoet = fuzzy.FuzzyText(length=3)

    class Meta:
        model = models.LPGVulpunt


class LPGVulpuntPointFactory(LPGVulpuntBase):
    geometrie_point = Point(0.0, 1.1)


class LPGVulpuntPolygonFactory(LPGVulpuntBase):
    geometrie_polygon = multipoly


class LPGTankFactory(factory.DjangoModelFactory):
    type = fuzzy.FuzzyText(length=40)
    afstandseis = fuzzy.FuzzyText(length=10)
    voldoet = fuzzy.FuzzyText(length=3)
    geometrie = multipoly

    class Meta:
        model = models.LPGTank


class LPGAfleverzuilBase(factory.DjangoModelFactory):
    station_id = fuzzy.FuzzyInteger(0, 10)

    class Meta:
        model = models.LPGAfleverzuil


class LPGAfleverzuilPointFactory(LPGAfleverzuilBase):
    geometrie_point = Point(0.0, 1.1)


class LPGAfleverzuilPolygonFactory(LPGAfleverzuilBase):
    geometrie_polygon = multipoly
