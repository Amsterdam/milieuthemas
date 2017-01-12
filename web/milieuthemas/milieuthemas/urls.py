import debug_toolbar
from django.conf.urls import url, include
from rest_framework import renderers, schemas, response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer
from django.conf import settings
from django.conf.urls.static import static


@api_view()
@renderer_classes([
    SwaggerUIRenderer,
    OpenAPIRenderer,
    renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Milieuthemas API')
    return response.Response(generator.get_schema(request=request))

urlpatterns = [
    url(r'^milieuthemas/docs/swagger/$', schema_view),
    url(r'^milieuthemas/', include('atlas_api.urls'), name="homepage"),
    url(r'^status/',
        include('datapunt_generic.health.urls', namespace='health'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
