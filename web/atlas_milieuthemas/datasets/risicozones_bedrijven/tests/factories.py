import factory

from .. import models


class LPGStationFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.LPGStation

