from os import name
from onefin.apps.views import MovieAPIView, RegistrationAPIViewset
from django.urls import path
from rest_framework import routers


app_name = "apps"

# The API URLs are now determined automatically by the router.

router = routers.SimpleRouter()
router.register('api/register', RegistrationAPIViewset)

urlpatterns = [
    path('movies/',
         MovieAPIView.as_view(),
         name='movie_api'
         )
]

urlpatterns += router.urls
