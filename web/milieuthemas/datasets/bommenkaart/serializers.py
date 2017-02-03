from datapunt_generic.generic import rest
from . import models


class BommenkaartMixin(rest.DataSetSerializerMixin):
    dataset = 'bommenkaart'


# list serializers
class BomInslag(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.BomInslag
        fields = (
            '_display',
            '_links',
            'kenmerk',
            'type',
        )


class GevrijwaardGebied(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.GevrijwaardGebied
        fields = (
            '_display',
            '_links',
            'kenmerk',
            'type',
        )


class UitgevoerdOnderzoek(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.UitgevoerdOnderzoek
        fields = (
            '_display',
            '_links',
            'kenmerk',
            'type',
        )


class VerdachtGebied(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.VerdachtGebied
        fields = (
            '_display',
            '_links',
            'kenmerk',
            'type',
        )


# detail serializers
class BomInslagDetail(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.BomInslag
        fields = (
            '_display',
            '_links',
            'id',
            'bron',
            'oorlogsinc',
            'type',
            'kenmerk',
            'opmerkingen',
            'nauwkeurig',
            'datum',
            'datum_inslag',
            'pdf',
            'intekening'
        )


class GevrijwaardGebiedDetail(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.GevrijwaardGebied
        fields = (
            '_display',
            '_links',
            'id',
            'bron',
            'kenmerk',
            'type',
            'datum',
            'opmerkingen',
            'nauwkeurig',
            'intekening',
        )


class UitgevoerdOnderzoekDetail(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.UitgevoerdOnderzoek
        fields = (
            '_display',
            '_links',
            'id',
            'kenmerk',
            'type',
            'opdrachtnemer',
            'verdacht_gebied',
            'onderzoeksgebied',
            'opdrachtgever',
            'datum',
        )


class VerdachtGebiedDetail(BommenkaartMixin, rest.HALSerializer):
    _display = rest.DisplayField(source='kenmerk')

    class Meta:
        model = models.VerdachtGebied
        fields = (
            '_display',
            '_links',
            'id',
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
