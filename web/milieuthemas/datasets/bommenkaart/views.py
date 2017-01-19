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
    type = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    kenmerk = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    datum = filters.DateFilter()

    class Meta:
        model = models.BomInslagDBView
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
    queryset = models.BomInslagDBView.objects.all()
    serializer_detail_class = serializers.BomInslagDetail
    serializer_class = serializers.BomInslag
    filter_backends = (DjangoFilterBackend,)
    filter_class = InslagFilter


class GevrijwaardGebiedFilter(FilterSet):
    type = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    kenmerk = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    datum = filters.DateFilter()
    datum_inslag = filters.DateFilter()

    class Meta:
        model = models.GevrijwaardGebiedDbView
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
    queryset = models.GevrijwaardGebiedDbView.objects.all()
    serializer_detail_class = serializers.GevrijwaardGebiedDetail
    serializer_class = serializers.GevrijwaardGebied
    filter_backends = (DjangoFilterBackend,)
    filter_class = GevrijwaardGebiedFilter


class UitgevoerdOnderzoekFilter(FilterSet):
    type = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    kenmerk = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    opdrachtgever = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    opdrachtnemer = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    datum = filters.DateFilter()

    class Meta:
        model = models.UitgevoerdOnderzoekDbView
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
    queryset = models.UitgevoerdOnderzoekDbView.objects.all()
    serializer_detail_class = serializers.UitgevoerdOnderzoekDetail
    serializer_class = serializers.UitgevoerdOnderzoek
    filter_backends = (DjangoFilterBackend,)
    filter_class = UitgevoerdOnderzoekFilter


class VerdachtGebiedFilter(FilterSet):
    kenmerk = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    type = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    kaliber = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    oorlogshandeling = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    aantal = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    subtype = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    verschijning = filters.CharFilter(lookup_expr=['exact', 'iexact'])
    afbakening = filters.CharFilter(lookup_expr=['exact', 'iexact'])

    class Meta:
        model = models.VerdachtGebiedDbView
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
    queryset = models.VerdachtGebiedDbView.objects.all()
    serializer_detail_class = serializers.VerdachtGebiedDetail
    serializer_class = serializers.VerdachtGebied
    filter_backends = (DjangoFilterBackend,)
    filter_class = VerdachtGebiedFilter
