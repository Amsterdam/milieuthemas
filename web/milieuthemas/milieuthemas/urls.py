import debug_toolbar
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
                  url(r'^milieuthemas/', include('datapunt_api.urls'),
                      name="milieuthemas"),
                  url(r'^status/',
                      include('datapunt_generic.health.urls',
                              namespace='health')),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
