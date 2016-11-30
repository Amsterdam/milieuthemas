from django.conf.urls import url, include
from rest_framework import routers


class DocumentedRouter(routers.DefaultRouter):
    """
    We do not have a rest api
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Datapunt(cls):
            pass

        Datapunt.__doc__ = self.__doc__
        return Datapunt.as_view()


router = DocumentedRouter()


urlpatterns = [
   # url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
   url(r'^', include(router.urls)),
]
