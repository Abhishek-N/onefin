from onefin.apps.views import RegistrationAPIView
from django.urls import path
from rest_framework import routers


app_name = "apps"

# The API URLs are now determined automatically by the router.

router = routers.SimpleRouter()
router.register('register', RegistrationAPIView)

urlpatterns = router.urls