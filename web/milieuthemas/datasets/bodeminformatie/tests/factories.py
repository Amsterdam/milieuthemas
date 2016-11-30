import factory
from factory import fuzzy

from django.contrib.gis.geos import Point

from .. import models


class GrondmonsterFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Grondmonster

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    eindoordeel = fuzzy.FuzzyText(length=4)
    geometrie = Point(0.0, 1.1)


class GrondwatermonsterFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Grondwatermonster

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    eindoordeel = fuzzy.FuzzyText(length=4)
    geometrie = Point(0.0, 1.1)


class AsbestFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Asbest

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    concentratie = fuzzy.FuzzyInteger(-10, 310)
    geometrie = Point(0.0, 1.1)

