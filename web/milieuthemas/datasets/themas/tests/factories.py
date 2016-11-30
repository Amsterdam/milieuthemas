import factory

from .. import models


class ThemaFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Thema
