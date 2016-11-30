import factory
from factory import fuzzy

from django.contrib.gis.geos import Point, MultiPolygon, Polygon

from .. import models

multipoly = MultiPolygon(
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
)


class VeiligheidsafstandPointFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Veiligheidsafstand

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    type = fuzzy.FuzzyText(length=100)
    locatie = fuzzy.FuzzyText(length=100)
    geometrie_point = Point(0.0, 1.1)


class VeiligheidsafstandPolygonFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Veiligheidsafstand

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    type = fuzzy.FuzzyText(length=100)
    locatie = fuzzy.FuzzyText(length=100)
    geometrie_multipolygon = multipoly
