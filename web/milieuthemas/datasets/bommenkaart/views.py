from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from rest_framework import metadata

from datapunt_generic.generic import rest
from . import serializers, models


class ExpansionMetadata(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        result = super().determine_metadata(request, view)
        result['parameters'] = dict(
            full=dict(
                type="string",
                description="If present, related entities are inlined",
                required=False
            )
        )
        return result


class InslagFilter(FilterSet):
    type = filters.CharFilter(lookup_expr='iexact')
    kenmerk = filters.CharFilter(lookup_expr='iexact')
    datum = filters.DateFilter()

    class Meta:
        model = models.BomInslag
        fields = (
            'kenmerk',
            'type',
            'datum'
        )


class InslagViewset(rest.AtlasViewSet):
    """
    Inslagen uitleg
    """

    metadata_class = ExpansionMetadata
    queryset = models.BomInslag.objects.all()
    serializer_detail_class = serializers.BomInslagDetail
    serializer_class = serializers.BomInslag
    filter_backends = (DjangoFilterBackend,)
    filter_class = InslagFilter


class GevrijwaardGebiedFilter(FilterSet):
    type = filters.CharFilter(lookup_expr='iexact')
    kenmerk = filters.CharFilter(lookup_expr='iexact')
    datum = filters.DateFilter()
    datum_inslag = filters.DateFilter()

    class Meta:
        model = models.GevrijwaardGebied
        fields = (
            'kenmerk',
            'type',
            'datum',
            'datum_inslag'
        )


class GevrijwaardGebiedViewSet(rest.AtlasViewSet):
    """
    Uitleg gevrijwaardgebied
    """

    metadata_class = ExpansionMetadata
    queryset = models.GevrijwaardGebied.objects.all()
    serializer_detail_class = serializers.GevrijwaardGebiedDetail
    serializer_class = serializers.GevrijwaardGebied
    filter_backends = (DjangoFilterBackend,)
    filter_class = GevrijwaardGebiedFilter


class UitgevoerdOnderzoekFilter(FilterSet):
    type = filters.CharFilter(lookup_expr='iexact')
    opdrachtgever = filters.CharFilter(lookup_expr='iexact')
    opdrachtnemer = filters.CharFilter(lookup_expr='iexact')
    datum = filters.DateFilter()

    class Meta:
        model = models.UitgevoerdOnderzoek
        fields = (
            'kenmerk',
            'type',
            'datum',
            'opdrachtgever',
            'opdrachtnemer'
        )


class UitgevoerdOnderzoekViewSet(rest.AtlasViewSet):
    """
    Uitleg uitgevoerd onderzoek
    """

    metadata_class = ExpansionMetadata
    queryset = models.UitgevoerdOnderzoek.objects.all()
    serializer_detail_class = serializers.UitgevoerdOnderzoekDetail
    serializer_class = serializers.UitgevoerdOnderzoek
    filter_backends = (DjangoFilterBackend,)
    filter_class = UitgevoerdOnderzoekFilter


class VerdachtGebiedFilter(FilterSet):
    kenmerk = filters.CharFilter(lookup_expr='iexact')
    type = filters.CharFilter(lookup_expr='iexact')
    kaliber = filters.CharFilter(lookup_expr='iexact')
    oorlogshandeling = filters.CharFilter(lookup_expr='iexact')
    aantal = filters.CharFilter(lookup_expr='iexact')
    subtype = filters.CharFilter(lookup_expr='iexact')
    verschijning = filters.CharFilter(lookup_expr='iexact')
    afbakening = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = models.VerdachtGebied
        fields = (
            'kenmerk',
            'type',
            'kaliber',
            'oorlogshandeling',
            'aantal',
            'subtype',
            'verschijning',
            'afbakening'
        )


class VerdachtGebiedViewSet(rest.AtlasViewSet):
    """
    Uitleg verdacht gebied
    """

    metadata_class = ExpansionMetadata
    queryset = models.VerdachtGebied.objects.all()
    serializer_detail_class = serializers.VerdachtGebiedDetail
    serializer_class = serializers.VerdachtGebied
    filter_backends = (DjangoFilterBackend,)
    filter_class = VerdachtGebiedFilter
