import factory
from factory import fuzzy

from django.contrib.gis.geos import Point, LineString, MultiPolygon, Polygon

from .. import models

multipoly = MultiPolygon(
    Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
    Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
)


class HoogtebeperkendeVlakkenPointFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.HoogtebeperkendeVlakken

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    geometrie_point = Point(0.0, 1.1)


class HoogtebeperkendeVlakkenLineFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.HoogtebeperkendeVlakken

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    geometrie_line = LineString((0, 0), (1, 1))


class HoogtebeperkendeVlakkenPolyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.HoogtebeperkendeVlakken

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    geometrie_polygon = multipoly


class GeluidzoneFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Geluidzone

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    geometrie = multipoly


class VogelvrijwaringsgebiedFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Geluidzone

    id = fuzzy.FuzzyInteger(0, 10)
    geo_id = fuzzy.FuzzyInteger(0, 10)
    geometrie = multipoly
