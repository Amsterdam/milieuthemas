import factory
from factory import fuzzy

from .. import models


class MeetboutFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.HoogtebeperkendeVlakken

    id = fuzzy.FuzzyText(length=10)
