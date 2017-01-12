import debug_toolbar
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import schemas, response
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

openapis = [
    url(r'^milieuthemas/', include('atlas_api.urls'), name="milieuthemas"),
]


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(
        title='Milieuthemas API', patterns=openapis)
    return response.Response(generator.get_schema(request=request))


urlpatterns = openapis + [
    url(r'^milieuthemas/docs/swagger/$', schema_view),
    url(r'^status/',
        include('datapunt_generic.health.urls', namespace='health')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
