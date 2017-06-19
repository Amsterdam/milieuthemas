from django.conf.urls import url, include
from rest_framework import schemas, response, routers
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer
from rest_framework_swagger.renderers import OpenAPIRenderer

from datasets.bommenkaart.urls import register_apis


class MilieuThemaView(routers.APIRootView):
    """
    Informatie over milieu gerelateerde zaken.
    Momenteel via deze api enkel explosieven in de stad.
    Inslagen (met mogelijke blindgangers), gevrijwaarde,
    verdachte en ondezochte gebieden.
    """


class MilieuThemaRouter(routers.DefaultRouter):
    APIRootView = MilieuThemaView


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
