from rest_framework import routers
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


class ExplosievenRouter(routers.DefaultRouter):
    """
    Informatie over explosieven in de stad. Inslagen (met mogelijke
    blindgangers), gevrijwaarde, verdachte en ondezochte gebieden.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Bommenkaart(cls):
            pass

        Bommenkaart.__doc__ = self.__doc__
        return Bommenkaart.as_view()


explosieven = ExplosievenRouter()

explosieven.register(r'inslagen', InslagViewset)
explosieven.register(r'gevrijwaardgebied', GevrijwaardGebiedViewSet)
explosieven.register(r'uitgevoerdonderzoek', UitgevoerdOnderzoekViewSet)
explosieven.register(r'verdachtgebied', VerdachtGebiedViewSet)
