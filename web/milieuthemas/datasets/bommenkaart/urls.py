from datasets.bommenkaart.views import *


class QueryMetadata(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        result = super().determine_metadata(request, view)
        result['parameters'] = {
            'q': {
                'type': 'string',
                'description': 'The query to search for',
                'required': False,
            },
        }
        return result


def register_apis(router):
    router.register(r'explosieven/inslagen', InslagViewset)
    router.register(r'explosieven/gevrijwaardgebied', GevrijwaardGebiedViewSet)
    router.register(r'explosieven/verdachtgebied', VerdachtGebiedViewSet)
    router.register(r'explosieven/uitgevoerdonderzoek',
                    UitgevoerdOnderzoekViewSet)
