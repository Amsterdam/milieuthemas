from django.conf.urls import url, include

from datasets.bommenkaart.urls import explosieven

urlpatterns = [
    url(r'^explosieven/', include(explosieven.urls)),
]
