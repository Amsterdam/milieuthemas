from datapunt_generic.generic import rest
from . import models


class BommenkaartMixin(rest.DataSetSerializerMixin):
    dataset = 'bommenkaart'


# list serializers
class BomInslag(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.BomInslagDBView
        fields = (
            '_links',
            'kenmerk',
            'type',
        )


class GevrijwaardGebied(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.GevrijwaardGebiedDbView
        fields = (
            '_links',
            'kenmerk',
            'type',
        )


class UitgevoerdOnderzoek(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.UitgevoerdOnderzoekDbView
        fields = (
            '_links',
            'kenmerk',
            'type',
        )


class VerdachtGebied(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.VerdachtGebiedDbView
        fields = (
            '_links',
            'kenmerk',
            'type',
        )


# detail serializers
class BomInslagDetail(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.BomInslagDBView
        fields = (
            '_links',
            'id',
            'uri',
            'bron',
            'oorlogsinc',
            'type',
            'kenmerk',
            'opmerkingen',
            'nauwkeurig',
            'datum',
            'pdf',
            'intekening'
        )


class GevrijwaardGebiedDetail(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.GevrijwaardGebiedDbView
        fields = (
            '_links',
            'id',
            'uri',
            'bron',
            'kenmerk',
            'type',
            'datum',
            'opmerkingen',
            'nauwkeurig',
            'intekening',
        )


class UitgevoerdOnderzoekDetail(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.UitgevoerdOnderzoekDbView
        fields = (
            '_links',
            'id',
            'uri',
            'kenmerk',
            'type',
            'opdrachtnemer',
            'verdacht_gebied',
            'onderzoeksgebied',
            'opdrachtgever',
            'datum',
        )


class VerdachtGebiedDetail(BommenkaartMixin, rest.HALSerializer):
    class Meta:
        model = models.VerdachtGebiedDbView
        fields = (
            '_links',
            'id',
            'uri',
            'bron',
            'kenmerk',
            'type',
            'afbakening',
            'aantal',
            'cartografie',
            'horizontaal',
            'kaliber',
            'subtype',
            'oorlogshandeling',
            'verschijning',
            'pdf',
            'opmerkingen',
        )
