from os import name

from django.urls import path
from onefin.apps.views import (CollectionsViewSet,
                               MovieAPIView, RegistrationAPIViewset)
from rest_framework import routers

app_name = "apps"

# The API URLs are now determined automatically by the router.

router = routers.SimpleRouter()
router.register('api/register', RegistrationAPIViewset)
router.register('collection', CollectionsViewSet)

urlpatterns = [
    path('movies/',
         MovieAPIView.as_view(),
         name='movie_api'
         ),
    #     path('collection/<int:collection_id>/',
    #          CollectionAPIView.as_view())
]

urlpatterns += router.urls
