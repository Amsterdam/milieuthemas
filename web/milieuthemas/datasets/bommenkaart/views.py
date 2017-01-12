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


class InslagViewset(rest.AtlasViewSet):
    """
    Inslagen uitleg
    """

    metadata_class = ExpansionMetadata
    queryset = models.BomInslagDBView.objects.all()
    serializer_detail_class = serializers.BomInslagDetail
    serializer_class = serializers.BomInslag
    filter_fields = set()


class GevrijwaardGebiedViewSet(rest.AtlasViewSet):
    """
    Uitleg gevrijwaardgebied
    """

    metadata_class = ExpansionMetadata
    queryset = models.GevrijwaardGebiedDbView.objects.all()
    serializer_detail_class = serializers.GevrijwaardGebiedDetail
    serializer_class = serializers.GevrijwaardGebied
    filter_fields = set()


class UitgevoerdOnderzoekViewSet(rest.AtlasViewSet):
    """
    Uitleg uitgevoerd onderzoek
    """

    metadata_class = ExpansionMetadata
    queryset = models.UitgevoerdOnderzoek.objects.all()
    serializer_detail_class = serializers.UitgevoerdOnderzoekDetail
    serializer_class = serializers.UitgevoerdOnderzoek
    filter_fields = set()


class VerdachtGebiedViewSet(rest.AtlasViewSet):
    """
    Uitleg verdacht gebied
    """

    metadata_class = ExpansionMetadata
    queryset = models.VerdachtGebied.objects.all()
    serializer_detail_class = serializers.VerdachtGebiedDetail
    serializer_class = serializers.VerdachtGebied
    filter_fields = set()
