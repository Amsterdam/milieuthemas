from django.conf.urls import url, include
from rest_framework import schemas, response, routers
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from datasets.bommenkaart.urls import register_apis


class MilieuThemaRouter(routers.DefaultRouter):
    """
    Informatie over milieu gerelateerde zaken.
    Momenteel via deze api enkel explosieven in de stad. Inslagen (met mogelijke
    blindgangers), gevrijwaarde, verdachte en ondezochte gebieden.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Milieuthemas(cls):
            pass

        Milieuthemas.__doc__ = self.__doc__
        return Milieuthemas.as_view()


milieuthemas = MilieuThemaRouter()
register_apis(milieuthemas)

base_url_patterns = [
    url(r'', include(milieuthemas.urls)),
]


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(
        title='Milieuthemas API',
        patterns=base_url_patterns)
    return response.Response(generator.get_schema(request=request))


urlpatterns = base_url_patterns + [
    url(r'^docs/api-docs/$', schema_view),
]
